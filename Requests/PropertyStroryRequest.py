from pydantic import BaseModel,Field
from sqlalchemy import Column, Float,Integer,String,Boolean, DateTime
from typing import Optional
from datetime import datetime

class CreatePropertyStory(BaseModel):

    property_id : int
    tipo: str
    fecha_inicio: datetime
    fecha_fin: datetime
    description: str

class DtoTaxRequest(BaseModel):
    id: int
    property_id : int
    tipo: str
    fecha_inicio: datetime
    fecha_fin: datetime