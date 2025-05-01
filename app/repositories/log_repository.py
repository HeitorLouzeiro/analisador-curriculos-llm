from typing import Dict

from pymongo.collection import Collection

from ..config.database import get_database_connection
from ..models.log import LogAnalise


class LogRepository:
    def __init__(self):
        db = get_database_connection()
        self.collection: Collection = db["logs"]

    def inserir_log(self, log: LogAnalise) -> Dict:
        """Insere um log na coleção de logs."""
        try:
            log_dict = log.dict(by_alias=True)
            result = self.collection.insert_one(log_dict)
            log_dict["_id"] = str(result.inserted_id)
            return log_dict
        except Exception as e:
            print(f"Erro ao salvar log no MongoDB: {e}")
            return log.dict(by_alias=True)
