import time
from openai import APIConnectionError
from app.rag.embeddings import get_embeddings_models
from app.rag.loader import load_pdfs
from app.rag.retriever import get_qdrant_client
from app.rag.splitter import split_documents
from app.rag.vectorstore import create_collection_if_not_exits, store_embeddings

def ingest_documents():
    print("🚀 Iniciando proceso de ingestión robusto...")
    
    client = get_qdrant_client()
    print("1 Cargando PDFs desde data/pdf...")
    documents = load_pdfs('data/pdf')
    print(f"2  Se cargaron {len(documents)} páginas.")
    
    print("Dividiendo documentos en chunks...")
    chunks = split_documents(documents)
    print(f"3 Se generaron {len(chunks)} chunks.")
    
    embeddings_model = get_embeddings_models()
    vectors = []
    
    print("Generando embeddings con reintentos...")
    for idx, chunk in enumerate(chunks):
        max_retries = 5
        retry_delay = 2
        success = False
        
        for attempt in range(max_retries):
            try:
                # Procesar uno por uno para mayor control
                vector = embeddings_model.embed_query(chunk["content"])
                vectors.append(vector)
                success = True
                print(f"   [{idx+1}/{len(chunks)}] Chunk procesado.")
                break
            except APIConnectionError as e:
                print(f"   ⚠️ Error de conexión en chunk {idx+1}, reintento {attempt+1}/{max_retries}...")
                time.sleep(retry_delay)
                retry_delay *= 2
            except Exception as e:
                print(f"   ❌ Error inesperado en chunk {idx+1}: {str(e)}")
                break
        
        if not success:
            print(f"   🛑 No se pudo procesar el chunk {idx+1} tras varios intentos.")
            return

    vector_size = len(vectors[0])
    create_collection_if_not_exits(client, vector_size)
    
    print(" Almacenando en Qdrant...")
    store_embeddings(chunks, vectors)
    print(" Proceso de ingestión completado exitosamente.")

if __name__ == "__main__":
    ingest_documents()
