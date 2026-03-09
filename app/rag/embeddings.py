

from langchain_openai import OpenAIEmbeddings

from app.config import OPEN_API_KEY


def get_embeddings_models():
    """
    Crea y devuelve el modelo de embedding de OpenAI.
    """
    return OpenAIEmbeddings(
        model = "text-embedding-3-small",
        api_key=OPEN_API_KEY,
        # request_timeout=60, # Algunas versiones usan esto
    )

def embed_chunks(chunks: list[dict]) -> list[list[float]]:
    """
    Recibe los chunks y devuelve la lista de vectores.
    """

    embeddings_model = get_embeddings_models()
    # print("Iniciando generación de embeddings...")

    texts = [chunk["content"] for chunk in chunks]

    # print(f"Enviando {len(texts)} textos a OpenAI...")

    vectors = embeddings_model.embed_documents(texts)
    # print("Embeddings recibidos.")

    return vectors
