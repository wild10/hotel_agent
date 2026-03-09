from openai import OpenAI

from app.config import OPEN_API_KEY
from app.rag.embeddings import embed_chunks
from app.rag.loader import load_pdfs
from app.rag.retriever import get_qdrant_client, retrieve_chunks
from app.rag.splitter import split_documents
from app.rag.vectorstore import create_collection_if_not_exits, store_embeddings

client = OpenAI(api_key=OPEN_API_KEY)

def build_context(chunks):
    """
    Une los chunks recuperados en un solo contexto.

    """
    context = "\n\n".join([chunk["content"] for chunk in chunks ])
    return context


def generate_answer(question:str):
    # recuperar chunks relevantes directamente de Qdrant
    chunks = retrieve_chunks(question, top_k=3)

    # construir contexto
    context = build_context(chunks)

    # crear Prompts.
    prompt = f"""
    you are helpful hotet assistant that replay in spanish.
    suse the following context to answer the question.
    context:
    {context}
    question:
    {question}
    answer:
    """

    # Llamar al LLM.
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role":"system", "content":"Eres un asistente de hotel que responde preguntas sobre políticas basándose en el contexto proporcionado."},
                  {"role": "user", "content":prompt}
        ],
        temperature=0
    )

    return response.choices[0].message.content 
