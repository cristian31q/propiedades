from pydantic import BaseModel,Field
from sqlalchemy import Column, Float,Integer,String,Boolean, DateTime
from typing import Optional

class CreateTenantRequest(BaseModel):

    transaction_state : int 
    transaction_type: str
    value: float
    income: bool
    account_num: str
    
    property_id : int
    salesperson_id : Optional[int] = None
    efectivo : Optional[float] = None
    transferencia : Optional[float] = None
    permuta : Optional[float] = None

class DtoTenantRequest(BaseModel):
    id: int
    transaction_state : int 
    transaction_type: str
    value: float
    income: bool
    account_num: str
    
    property_id : int
    salesperson_id : Optional[int] = None
    efectivo : Optional[float] = None
    transferencia : Optional[float] = None
    permuta : Optional[float] = None