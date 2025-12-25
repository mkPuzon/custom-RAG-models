'''generate_corpus.py

Contains functions for generating a plain text corpus from multiple sources. Currently supports:
- Wikipedia
- Local pdfs

Dec 2025
'''
import os
import re
import wikipedia

from docling.document_converter import DocumentConverter

def sanitize_filename(input_string):
    return re.sub(r'[^a-zA-Z0-9]', '_', input_string)

def generate_corpus_wiki(search_term="Buddhism", num_articles=1000, output_dir="all_articles"):
    os.makedirs(output_dir, exist_ok=True)

    articles = []
    search_results = wikipedia.search(search_term, results=num_articles)

    for i, title in enumerate(search_results, 1):
        try:
            page = wikipedia.page(title, auto_suggest=False)
            articles.append((title, page.content))

            sanitized = sanitize_filename(title)
            filename = f"{sanitized}.txt"
            filepath = os.path.join(output_dir, filename)

            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(page.content)
        except Exception as e:
            print(f"Error processing '{title}': {str(e)}")
            continue
    print(f"\nProcess complete. Saved {len(articles)} articles.")

def generate_corpus_pdf(input_dir: str, output_dir: str = "corpuses/pdf_output"):
    # TODO 
    os.makedirs(output_dir, exist_ok=True)
    for root, dirs, files in os.walk(input_dir):
        for file in files:
            filepath = os.path.join(root, file)
            conv = DocumentConverter()
            doc = conv.convert(filepath).document
    
if __name__ == "__main__":
    # generate_corpus_wiki(search_term="optic flow", num_articles=20, output_dir="corpuses/optic_flow")
    generate_corpus_pdf(input_dir="corpuses/pdfs", output_dir="corpuses/OWLabResources")