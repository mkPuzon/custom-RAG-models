'''prepare_context.py

Ensures there are no redundancies within retrieved context.

Dec 2025
'''
import sys
from sentence_transformers import SentenceTransformer

from pull_db_content import search_embeddings, get_surrounding_sentences
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

def search_by_query(query: str, num_matches: int = 5, group_window_sz: int = 5):
    session = get_psql_session()
    model = SentenceTransformer("Qwen3-Embedding-0.6B", device='cpu')
    query_embedding = model.encode(query)

    search_results = search_embeddings(query_embedding, session=session, limit=num_matches * (2 * group_window_sz + 1))
    filtered_matches = get_filtered_matches(search_results=search_results)

    entry_ids = [i[0] for i in filtered_matches]
    file_names = [i[3] for i in filtered_matches]

    return get_surrounding_sentences(
        entry_ids=entry_ids, 
        file_names=file_names, 
        group_window_sz=group_window_sz, 
        session=session)