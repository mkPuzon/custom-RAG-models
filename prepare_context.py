'''prepare_context.py

Ensures there are no redundancies within retrieved context.

Dec 2025
'''
import sys
import gc
from sentence_transformers import SentenceTransformer

from pull_db_content import search_embeddings
from populate_db import get_psql_session, TextEmbedding

def is_unique_to_window(existing_matches, current_match, group_window_sz: int = 5) -> bool:
    '''
    Helper function to identify if a current_match is part of the context window of already 
    existing_matches.
    '''
    for match in existing_matches:
        # match[3] == filename
        if match[3] != current_match[3]: 
            continue
        # match[1] == 
        if match[1] > current_match[1] + group_window_sz or match[1] < current_match[1] - group_window_sz:
            continue
        else:
            return False
    return True

def get_filtered_matches(search_results, num_matches: int = 5) -> list[str]:
    unique_count = 0
    matches = []
    for result in search_results:
        if unique_count >= 5:
            break
        if is_unique_to_window(existing_matches=matches, current_match=result):
            unique_count += 1
        matches.append(result)
    return matches

def group_entries(entry_ids: list[int], file_names: list[str], index_of_interest: int, group_window_sz: int) -> list[int]:
    '''
    Identify if an entry with index_of_intereset needs grouping with other entries.
    '''
    entry_id_oi = entry_ids[index_of_interest]
    file_name_oi = file_names[index_of_interest]
    group_idx = [index_of_interest]

    for idx, (entry_id, file_name) in enumerate(zip(entry_ids, file_names)):
        if file_name != file_name_oi:
            continue
        if (entry_id >= entry_id_oi - group_window_sz) and (entry_id <= entry_id_oi + group_window_sz):
            group_idx.append(idx)
    
    return group_idx

def consolidate_groupings(grouped_entries):
    # Given a list of lists with grouped entries, combine all lists that have one or more elements in common, then remove duplicates.
    # This should result in a number of lists equal to the number of matched contexts we want

    # Assumes we have run the function group_entries on each entry

    original_groups = grouped_entries[:]
    combined_groups = []

    while( len(original_groups) ):
        current_grouping = original_groups[0][:]
        original_groups.remove(original_groups[0])
        for other_entry in original_groups:
            for idx in current_grouping:
                if idx in other_entry:
                    current_grouping += other_entry
                    original_groups.remove(other_entry)
                    break;
        
        current_grouping = list(set(current_grouping))
        combined_groups.append(current_grouping)

    return combined_groups

def get_min_max_ids(entry_ids, file_names, combined_groups, group_window_sz):

    min_ids = []
    max_ids = []

    for group in combined_groups:
        min_id = min([entry_ids[i] for i in group])
        max_id = max([entry_ids[i] for i in group])

        min_id = min_id - group_window_sz
        max_id = max_id + group_window_sz

        min_ids.append(min_id)
        max_ids.append(max_id)

    return min_ids, max_ids

def get_surrounding_sentences(entry_ids, file_names, group_window_sz, session):

    grouped_entries = []
    for idx, id in enumerate(entry_ids):
        grouped_entries.append(group_entries(entry_ids, file_names, index_of_interest = idx, group_window_sz = group_window_sz))

    combined_groups = consolidate_groupings(grouped_entries)
    min_ids, max_ids = get_min_max_ids(entry_ids, file_names, combined_groups, group_window_sz)
    surrounding_sentences = []

    # get the relevant sentences from database
    for min_id, max_id in zip(min_ids, max_ids):
        # add context to surrounding_sentences list
        surrounding_sentences.append(
            session.query(TextEmbedding.id, TextEmbedding.sentence_number, TextEmbedding.content, TextEmbedding.file_name)\
            .filter(TextEmbedding.id >= min_id)\
            .filter(TextEmbedding.id <= max_id)\
            .all()
        )
    
    return surrounding_sentences


def search_by_query(query: str, num_matches: int = 5, group_window_sz: int = 5):
    sessionmaker = get_psql_session()
    with sessionmaker() as session:
        model = SentenceTransformer("Qwen3-Embedding-0.6B", device='cpu')
        query_embedding = model.encode(query)
        # fix HF memory leak
        del model
        gc.collect()

        search_results = search_embeddings(query_embedding, session=session, limit=num_matches * (2 * group_window_sz + 1))
        filtered_matches = get_filtered_matches(search_results=search_results)

        entry_ids = [i[0] for i in filtered_matches]
        file_names = [i[3] for i in filtered_matches]

        return get_surrounding_sentences(
            entry_ids=entry_ids, 
            file_names=file_names, 
            group_window_sz=group_window_sz, 
            session=session)


if __name__=="__main__":
    query = "Tell me about the brain area that processes optic flow."

    context = search_by_query(query)

    for i in context:
        print(i, "\n")