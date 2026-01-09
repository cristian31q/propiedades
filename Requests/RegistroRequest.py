from pydantic import BaseModel, json
from typing import Optional
from datetime import datetime

class CreateRegistroRequest(BaseModel):
    property_id: int
    my_json: dict
    total: float
    fechaCorte: datetime
    fechaInicio: datetime

    class Config:
        arbitrary_types_allowed = True  # Permitir tipos arbitrarios (como SQLAlchemy)
