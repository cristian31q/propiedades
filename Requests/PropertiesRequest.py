from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class CreatePropertiesRequest(BaseModel):
    
    title: str
    address: str
    city: str
    neighborhood: str
    chip: str
    contract_period: str
    scripture_date: datetime
    scripture_value: float
    notaria: str
    property_type: int
    property_status: Optional[str]
    tax_id: Optional[int] = None
    contract_id: Optional[int] = None
    description: Optional[str] = None
    fecha_vacia: Optional[datetime] =None
    identificador_contadoras : Optional[str] =None
    identificador_inmob : Optional[str] =None
    matricula: Optional[str] =None
    # Configuración adicional para permitir tipos arbitrarios (como los de SQLAlchemy)
    class Config:
        arbitrary_types_allowed = True  # Esto permitirá manejar los tipos SQLAlchemy sin errores


class DtoPropertiesRequest(BaseModel):
    id: int
    title: str
    address: str
    city: str
    neighborhood: str
    chip: str
    contract_period: str
    scripture_date: datetime
    scripture_value: float
    notaria: str
    property_type: int
    property_status: Optional[str]
    tax_id: Optional[int] = None
    contract_id: Optional[int] = None
    description: Optional[str] = None
    fecha_vacia: Optional[datetime] =None
    identificador_contadoras : Optional[str] =None
    identificador_inmob : Optional[str] =None
    matricula: Optional[str] =None
    # Configuración adicional para permitir tipos arbitrarios (como los de SQLAlchemy)
    class Config:
        arbitrary_types_allowed = True  # Esto permitirá manejar los tipos SQLAlchemy sin errores
