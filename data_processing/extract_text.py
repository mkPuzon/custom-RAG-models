'''

Dec 2015
'''
from docling.document_converter import DocumentConverter

def convert_doc(source):
    converter = DocumentConverter()
    result = converter.convert(source)
    return result.document.export_to_dict()

if __name__ == "__main__":
    pptx = "https://scholar.harvard.edu/files/torman_personal/files/samplepptx.pptx"
    docx = "https://calibre-ebook.com/downloads/demos/demo.docx"
    
    result = convert_doc(docx)
    for i in result["texts"]:
        print(i['orig'])