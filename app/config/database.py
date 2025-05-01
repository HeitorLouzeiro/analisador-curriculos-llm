import os

from pymongo import MongoClient
from pymongo.database import Database


def get_database_connection() -> Database:
    """Retorna uma conexão com o banco de dados MongoDB."""
    mongo_url = os.environ.get("MONGO_URL", "mongodb://localhost:27017")
    client = MongoClient(mongo_url)
    return client["fabio_db"]


def inicializar_db() -> None:
    """Inicializa conexão com banco de dados e cria índices necessários."""
    db = get_database_connection()

    # Certifica-se de que a coleção de logs existe e tem os índices adequados
    if "logs" not in db.list_collection_names():
        db.create_collection("logs")

    # Cria índices para melhorar performance de consultas comuns
    db.logs.create_index("user_id")
    db.logs.create_index("request_id")
    db.logs.create_index("timestamp")

    print("Banco de dados inicializado com sucesso!")
