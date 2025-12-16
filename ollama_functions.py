'''
 
Dec 2025
'''
from pprint import pprint
from ollama import embed, chat

def batch_embed(input: list[str], model: str ="nomic-embed-text") -> tuple[int, list[list[float]]]:
    # embed return a 'ollama._types.EmbedResponse' object with the following keys:
    # 'model', 'created_at', 'done', 'done_reason', 'total_duration', 'load_duration', 'prompt_eval_count', 'prompt_eval_duration', 'eval_count', 'eval_duration', 'embeddings'
    batch = embed(model=model, input=input)
    return (len(batch["embeddings"]), batch["embeddings"])

def basic_query(message: str, model: str ="rag-qwen3:0.6b") -> str:
    response = chat(model=model, messages=[
        {
            'role': 'user',
            'content': f"{message}"
        }
    ])
    return response.message.content

if __name__ == "__main__":
    # print(basic_query(message="How are ya doin?"))
    n, embdings = batch_embed(input=["hi", "hello"])
    print(type(embdings[0][0]))