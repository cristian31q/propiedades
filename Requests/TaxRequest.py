from pydantic import BaseModel,Field
from sqlalchemy import Column, Float,Integer,String,Boolean, DateTime
from typing import Optional
from datetime import datetime

class CreateTaxRequest(BaseModel):

    description : str
    tax_year: datetime
    avaluo: float
    payment_day: datetime
    account_num: str

    Properties_id : int
    value: float
    forma_pago: str

    class Config:
        arbitrary_types_allowed = True  


class DtoTaxRequest(BaseModel):
    id:int
    description : Optional[str] = None
    tax_year: Optional[datetime] = None
    avaluo:Optional[float] = None
    payment_day: Optional[datetime] = None
    account_num: Optional[str] = None

    Properties_id : Optional[int] = None
    value: Optional[float] = None
    forma_pago: Optional[str] = None

    class Config:
        arbitrary_types_allowed = True  