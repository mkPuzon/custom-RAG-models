'''run_rag.py

Queries the RAG db with a custom model.

Dec 2025
'''
import sys
from ollama import chat
from prepare_context import search_by_query


def make_prompt(query:str, context):
    return f"<|content_start> {context}<|contend_end> {query}"

if __name__ == "__main__":
    query = "What brain area responds to optic flow?"
    resposne = chat(model='qwen3-rag:0.6b', messages=[
        {
            'role': 'user',
            'content': make_prompt(query, search_by_query(query))
        }
    ])
    print(resposne.message.content)
    