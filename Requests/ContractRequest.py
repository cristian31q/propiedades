from pydantic import BaseModel,Field
from sqlalchemy import DateTime
from typing import Optional
from datetime import datetime

class CreateContractRequest(BaseModel):

    canon_arrendamiento: float
    administracion : float
    begin_date : datetime
    renovation_date : datetime
    rise: str
    insurance: bool
    owner_id: Optional[int] = None
    gastos_mtto: Optional[float] = None
    recibos_domiciliarios: Optional[float] = None
    extraordinarios: Optional[float] = None
    comision_admin: Optional[float] = None
    insurance_canon: Optional[float] = None
    insurance_admin: Optional[float] = None
    gastos_varios: Optional[float] = None

    inmobiliaria_id : Optional[int] = None
    property_id: int
    months_notify: int


class DtoContractRequest(BaseModel):
    id: int
    canon_arrendamiento: float
    administracion : float
    begin_date : datetime
    renovation_date : datetime
    rise: float
    insurance: bool
    owner_id: Optional[int] = None
    gastos_mtto: Optional[float] = None
    recibos_domiciliarios: Optional[float] = None
    extraordinarios: Optional[float] = None
    comision_admin: Optional[float] = None
    insurance_canon: Optional[float] = None
    insurance_admin: Optional[float] = None
    gastos_varios: Optional[float] = None

    inmobiliaria_id : Optional[int] = None
    property_id: int

    months_notify: Optional[int] = None