from datetime import datetime
from typing import Dict, List, Optional

from pydantic import BaseModel


class AnaliseCurriculoResponse(BaseModel):
    request_id: str
    user_id: str
    timestamp: datetime
    query: Optional[str] = None
    resultado: List[Dict]


class AnaliseCurriculoRequest(BaseModel):
    request_id: str
    user_id: str
    query: Optional[str] = None
