import logging
from uuid import uuid4

from qdrant_client import QdrantClient
from qdrant_client.http.exceptions import UnexpectedResponse
from qdrant_client.models import Distance, PointStruct, VectorParams

from app.config import COLLECTION_NAME, QDRANT_HOST, QDRANT_PORT

## show info 
# logging.basicConfig(
#     level = logging.INFO,
# )

def get_qdrant_client():
    """
    Crear cliente de qdrant.
    """

    return QdrantClient(
        host= QDRANT_HOST,
        port=QDRANT_PORT
    )


def create_collection_if_not_exits(client, vector_size:int):
    """
    Crea la collection si no existe aun y ajusta al embedding.
    """
    # usamos try para lanzar un excepcion si no existe.
    try:
        # check the collection exits and print info.
        client.get_collection(COLLECTION_NAME)
        logging.info(f" La collection {COLLECTION_NAME} ya existe.")
    
    except UnexpectedResponse:
        # show the collection doesn´t exits and create the new collection.
        logging.error(f" La collection {COLLECTION_NAME} no existe!")

        client.create_collection(
            collection_name = COLLECTION_NAME,
            vectors_config = VectorParams(
                size= vector_size,
                distance=Distance.COSINE
            )
        )
        logging.info(f" collection creada--{client.get_collection(COLLECTION_NAME)}")



def store_embeddings(chunks:list[dict], vectors:list[list[float]], batch_size: int=100):
    """
    Almacenar el embedding en QDrant junto a su metadata.
    :param chunk: Lista de chunks con su contenido y metadata.
    :param vectors: lista de vectores generados por embedding.
    :param batch_size: tamaño del batch para insertion.
    """

    if len(chunks) != len(vectors):
        raise ValueError("Chunks y vectores deben tener el mimos tamaño.")
    
    # obtener acceso a q drant.
    client = get_qdrant_client()

    points = []

    # looping chunks & vectors:
    for chunk , vector in zip(chunks, vectors):
        point = PointStruct(
            id=str(uuid4()),
            vector=vector,
            payload={
                "content": chunk["content"],
                "metadata": chunk.get("metadata", {})
            }
        )
        points.append(point)

    # Insertar por batches.
    for i in range(0, len(points), batch_size):
        batch = points[i:i + batch_size]
        client.upsert(
            collection_name=COLLECTION_NAME,
            points=batch
        )
    logging.info(f"✅ Se almacenaron {len(points)} embeddings en QDrant.")

