'''pull_db_content.py

Dec 2025
'''
from sentence_transformers import SentenceTransformer
from database_embeddings import get_psql_session, TextEmbedding

def search_embeddings(query_embedding, session, limit=5):
    return session.query(TextEmbedding.id, TextEmbedding.sentence_number, TextEmbedding.content, TextEmbedding.file_name, \
                        TextEmbedding.embedding.cosine_distance(query_embedding).label('distance'))\
                        .order_by('distance').limit(limit).all() 

if __name__ == '__main__':
    query = "Tell me about optic flow"
    model = SentenceTransformer('Qwen3-Embedding-0.6B', device='cpu') # https://huggingface.co/Qwen/Qwen3-Embedding-0.6B
    query_embedding = model.encode(query)
    session = get_psql_session()
    query_result = search_embeddings