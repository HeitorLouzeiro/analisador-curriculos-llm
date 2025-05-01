import json
from datetime import datetime
from typing import Any, Union

from bson import ObjectId


class JSONEncoder(json.JSONEncoder):
    """Encoder personalizado para serializar tipos específicos para JSON."""

    def default(self, o: Any) -> Union[str, Any]:
        """Converte tipos especiais para representação JSON."""
        if isinstance(o, ObjectId):
            return str(o)
        if isinstance(o, datetime):
            return o.isoformat()
        return super().default(o)


def serializar_para_json(obj: Any) -> dict:
    """Converte um objeto para dict JSON serializável."""
    return json.loads(json.dumps(obj, cls=JSONEncoder))
