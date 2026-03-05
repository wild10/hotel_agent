# Load Documents : pdfs, html,markdown, etc.

from pathlib import Path
from typing import Dict, List

from pypdf import PdfReader

DATA_PATH = Path("data/pdf")

"""
Doc loader function.
Load every pdf, with source and pages.

"""

def load_pdfs(data_path:str)-> List[Dict]:
    documents = []
    DATA_PATH = Path(data_path)
    # Load the list of pdfs.
    pdf_files = DATA_PATH.glob("*.pdf")

    for pdf_file in pdf_files:
        # Read the pdf with reader
        reader = PdfReader(pdf_file)

        # organize pages and text
        for page_number, page in enumerate(reader.pages):
            text = page.extract_text()
            # Clean white spaces in leading & trailing.
            if text and text.strip():
                documents.append(
                    {
                        "content": text,
                        "metadata":{
                            "source":pdf_file.name,
                            "page": page_number + 1
                        }

                    }
                )
            
    return documents 

if __name__=='__main__':
    docs = load_pdfs()
    print(f"Se cargaron{len(docs)} paginas. ")
    print(docs[0])
    # print(docs[0]["metadata"], docs)