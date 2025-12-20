'''
Populates a Postgres db with sentence-tokenized data from a local directory.

Dec 2025
'''
import os
import gc
import nltk
import torch

from nltk.tokenize import sent_tokenize
from sentence_transformers import SentenceTransformer
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base
from pgvector.sqlalchemy import Vector

# check that tokenizer is downloaded
try:
    nltk.data.find('tokenizers/punkt_tab')
except LookupError:
    nltk.download('punkt_tab')
    nltk.download('punkt')
    
Base = declarative_base()

class TextEmbedding(Base):
    __tablename__ = 'text_embeddings'
    id = Column(Integer, primary_key=True, autoincrement=True)
    embedding = Column(Vector)
    content = Column(String)
    file_name = Column(String)
    sentence_number = Column(Integer)

    def __str___(self):
        return self.content + " " + str(self.id)

def get_psql_session() -> sessionmaker:
    '''Creates a connection to database.'''
    # engine = create_engine('postgresql://postgres:postgres@localhost/text_embeddings')
    engine = create_engine('postgresql+psycopg2://postgres:postgres@localhost:5432/text_embeddings')
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine)

def insert_embeddings(embeddings: list[float], contents: list[str], file_names: list[str], session: sessionmaker) -> None:
    '''Inserts sentence embeddings into Postgres db.'''
    for embedding, content, file_name in zip(embeddings, contents, file_names):
        new_embedding = TextEmbedding(embedding=embedding, content=content, file_name=file_name)
        session.add(new_embedding)
    session.commit()

def populate_vector_db(folder_path: str='all_articles') -> None:
    Session = get_psql_session()
    model = SentenceTransformer('Qwen3-Embedding-0.6B', device='cpu') # https://huggingface.co/Qwen/Qwen3-Embedding-0.6B

    if not os.path.exists(folder_path):
        print(f"Error: Folder {folder_path} not found.")
        return
    
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if not os.path.isfile(file_path):
            print(f"Warning: Skipping file {file_path} since it is not a file.")
            continue
        print(f"Processing {file_path} ...")

        try:
            with open(file_path, 'r') as f:
                content = f.read()
            sentences = sent_tokenize(content)
            if not sentences: # skip empty files
                continue

            # open a session for this specific file
            with Session() as session:
                # process in batch size of 8
                for i in range(0, len(sentences), 8):
                    batch_sentences = sentences[i:i+8]
                    # generate embeddings
                    batch_embeddings = model.encode(batch_sentences, batch_size=8)

                    for j, (embedding, content) in enumerate(zip(batch_embeddings, batch_sentences)):
                        new_embedding = TextEmbedding(
                            embedding=embedding.tolist(), 
                            content=content, 
                            file_name=filename, 
                            sentence_number=i+j+1)
                        session.add(new_embedding)
                # commit once per file
                session.commit()
            print(f"Successfully generated embeddings for {file_path}")
            # cleen up memory
            gc.collect()
            torch.cuda.empty_cache()
        
        except Exception as e:
            print(f"Error processing {filename}: {str(e)}")
            continue

if __name__ == "__main__":
    populate_vector_db(folder_path="buddhism_articles")
