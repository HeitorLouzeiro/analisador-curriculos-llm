import uuid
from datetime import datetime
from typing import List, Optional

from bson import ObjectId
from pydantic import BaseModel, Field


class AnaliseResultado(BaseModel):
    arquivo: str
    resposta: Optional[str] = None
    resumo: Optional[str] = None


class LogAnalise(BaseModel):
    request_id: Optional[str] = Field(
        default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    timestamp: datetime = Field(default_factory=datetime.now)
    query: Optional[str] = None
    resultado: List[AnaliseResultado]

    class Config:
        json_encoders = {
            ObjectId: str,
            datetime: lambda dt: dt.isoformat()
        }
        populate_by_name = True
