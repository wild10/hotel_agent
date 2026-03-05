import logging

logging.basicConfig(level=logging.INFO)
from app.llm import ask_llm
from app.rag.embeddings import embed_chunks
from app.rag.loader import load_pdfs
from app.rag.pipeline import generate_answer
from app.rag.retriever import retrieve_chunks
from app.rag.splitter import split_documents
from app.rag.vectorstore import (
    create_collection_if_not_exits,
    get_qdrant_client,
    store_embeddings,
)


def test_chunk():
    
    # Cargar documentos:
    documents = load_pdfs("data/pdf")
    print(f" documentos cargados correctamente{len(documents)}")


    # 2 Dividir chunks.
    chunks = split_documents(documents)
    print(f" total de chunks generados{len(chunks)}")

    # Mostrar los ultimos 2 chunks.
    for i, chunk in enumerate( chunks[:2]):
        print(chunk["content"], chunk["metadata"])
    

def test_embeddings():
    
    documentos = load_pdfs("data/pdf")

    chunks = split_documents(documentos)

    vectors = embed_chunks(chunks)
    print(f"✅ Se generaron {len(vectors)} vectores exitosamente.")
    print(f"Dimensiones del primer vector: {len(vectors[0])}")
    print(f" vector[0]:{vectors[0]}")

def test_qdrant_collection():
    
    # creamos el vector database.
    cliente_qdrant = get_qdrant_client()
    # cargamos el documento
    documentos = load_pdfs('data/pdf')
    # dividimos el doc en partes(chunks)
    chunks = split_documents(documentos)
    # creamos los embeddinsgs.
    vectors = embed_chunks(chunks)
    # get size para almancenar en qdrant
    vector_size =len( vectors[0])
    # verificar si existe vector bd.
    create_collection_if_not_exits(cliente_qdrant, vector_size)

def test_store_embeddings():

    qdrant_client  = get_qdrant_client()

    docs = load_pdfs('data/pdf')

    chunks = split_documents(docs)

    vectors = embed_chunks(chunks)

    vectors_size = len(vectors[0])

    create_collection_if_not_exits(qdrant_client,vectors_size)

    store_embeddings(chunks, vectors)

def test_retriever():
    test_store_embeddings()

    question = "Cuales son las politicas de cancelacion?"
    results = retrieve_chunks(question, top_k=3)

    for r in results:
        logging.info(f"Score: {r['score']}")
        logging.info(f"Contenido:{r['content'][:200]}")
        logging.info(f"Metadata: {r['metadata']}")

def test_rag():
    question = " Cuales son las politicas de cancelacion?"
    answer = generate_answer(question)
    print("\nANSWER\n")
    print(answer)

if __name__ == '__main__':
    # create the question
    # question = "Dime una curiosidad sobre hotesls"
    # answer = ask_llm(question)
    # logging.info("Respuesta del modelo.")
    # print(answer)
    # test_chunk()
    # test_embeddings()
    # test_qdrant_collection()
    # test_store_embeddings()
    # test_retriever()
    test_rag()



