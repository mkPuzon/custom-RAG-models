'''
Populates a Postgres db with sentence-tokenized data from a local directory.

Dec 2025
'''
import os
import gc
import torch
from ollama import embed
from nltk.tokenize import sent_tokenize
from sentence_transformers import SentenceTransformer
from database_embeddings import get_psql_session, TextEmbedding

def populate_vector_db(folder_path: str='all_articles') -> None:
    Session = get_psql_session()
    model = SentenceTransformer('Qwen3-Embedding-0.6B', device='cpu') # https://huggingface.co/Qwen/Qwen3-Embedding-0.6B

    for filename in os.listdir(folder_path):

        file_path = os.path.join(folder_path, filename)
        print(f"Attempting to add {file_path} ...")

        try:
            with open(file_path, 'r') as f:
                content = f.read()
            sentences = sent_tokenize(content)

            with Session() as session:
                for i in range(0, len(sentences), 8):
                    batch_sentences = sentences[i:i+8]
                    batch_embeddings = model.encode(batch_sentences, batch_size=8)

                    for j, (embedding, content) in enumerate(zip(batch_embeddings, batch_sentences)):
                        new_embedding = TextEmbedding(
                            embedding=embedding, 
                            content=content, 
                            file_name=filename, 
                            sentence_number=i+j+1)
                        session.add(new_embedding)
                    session.commit()

            gc.collect()
            torch.cuda.empty_cache()
            print(f"Successfully generated embeddings for {file_path}")
            
        except Exception as e:
            print(f"Error processing {filename}: {str(e)}")
            continue

if __name__ == "__main__":
    populate_vector_db(folder_path="buddhism_articles")
