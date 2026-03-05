from langchain_text_splitters import RecursiveCharacterTextSplitter


def split_documents(documents: list[dict]) -> list[dict]:
    """
    Split documents into smaller chunks for embedding (token-based).
    """

    text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        encoding_name="cl100k_base",  # mismo encoding que GPT-4 / GPT-4o
        chunk_size=800,               # 800 tokens reales
        chunk_overlap=150             # 150 tokens reales de overlap
    )

    chunks = []

    for doc in documents:
        splits = text_splitter.split_text(doc["content"])

        for i, chunk in enumerate(splits):
            chunks.append({
                "content": chunk,
                "metadata": {
                    "source": doc["metadata"].get("source"),
                    "page": doc["metadata"].get("page"),
                    "chunk_index": i
                }
            })

    return chunks


if __name__ == "__main__":
    docs = [{
        "content": """SERVICIOS DEL HOTEL
Desayuno buffet:
Disponible todos los días de 7:00 a 10:00.
Incluido en algunas tarifas.

Estacionamiento:
Disponible para huéspedes.
Costo adicional por noche.

Servicio de lavandería:
Disponible bajo solicitud.
Tiempo de entrega: 24 horas.
""",
        "metadata": {
            "source": "servicios_hotel.pdf",
            "page": 1
        }
    }]

    result = split_documents(docs)

    for r in result:
        print("\n--- CHUNK ---")
        print(r["content"])
        print("Metadata:", r["metadata"])