import logging
import os

from dotenv import load_dotenv

load_dotenv()


OPEN_API_KEY = os.getenv("OPENAI_API_KEY_TOKEN")

if not OPEN_API_KEY:
    logging.error("No se encontro token validos!")

QDRANT_HOST = os.getenv("MY_QDRANT_HOST")
QDRANT_PORT = os.getenv("MY_QDRANT_PORT") 
COLLECTION_NAME = os.getenv("VECTOR_BD_NAME")