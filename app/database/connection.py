import os

import psycopg
from dotenv import load_dotenv
from psycopg.rows import dict_row

# Cargar setup env.
load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

# Function para establer la conexion.
def get_connection():
    """
    Crear una nueva conexion postgres.
    """
    return psycopg.connect(
        host= DB_HOST,
        port = DB_PORT,
        dbname = DB_NAME,
        user = DB_USER,
        password = DB_PASSWORD,
        row_factory=dict_row
    )