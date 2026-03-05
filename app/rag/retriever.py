from qdrant_client import QdrantClient
from qdrant_client.models import Filter

from app.config import QDRANT_HOST, QDRANT_PORT
from app.rag.embeddings import get_embeddings_models
from app.rag.vectorstore import COLLECTION_NAME, get_qdrant_client


def retrieve_chunks(query: str, top_k:int=3):
    """
    Recibe una consulta(sentence) y devuelve los chunks + similares.
    """
    # Iniciar vector DB accesss.
    client = get_qdrant_client()
    # convert to embeddings.
    embedding_model = get_embeddings_models()
    query_vector = embedding_model.embed_query(query)

    # Buscar en Qdrant.
    search_result = client.query_points(
        collection_name = COLLECTION_NAME,
        query = query_vector,
        limit = top_k,

    )
    # Extraer contenido ordenado por score.
    results = []

    for hit in search_result.points:
        results.append({
            "score": hit.score,
            "content": hit.payload["content"],
            "metadata": hit.payload["metadata"]
        })

    return results