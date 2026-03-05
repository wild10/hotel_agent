
# from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_text_splitters import RecursiveCharacterTextSplitter


def split_documents(documents: list[dict]) -> list[dict]:
    """
    Split documents into smaller chunks for embedding.
    """
    text_splitter  = RecursiveCharacterTextSplitter(
        chunk_size = 800,       # tamaño de chunk.
        chunk_overlap = 150,    # solapamiento para no perder contexto.
        # length_function = len,
    )

    chunks = []

    for doc in documents:
        splits = text_splitter.split_text(doc["content"])

        # print(splits)
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


if __name__=='__main__':
    doc = [{'content': 'SERVICIOS DEL HOTEL\nDesayuno buffet:\nDisponible todos los días de 7:00 a 10:00.\nIncluido en algunas tarifas.\nEstacionamiento:\nDisponible para huéspedes.\nCosto adicional por noche.\nServicio de lavandería:\nDisponible bajo solicitud.\nTiempo de entrega: 24 horas.', 'metadata': {'source': 'servicios_hotel.pdf', 'page': 1}}]
    split_documents(doc[0])