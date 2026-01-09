from pydantic import BaseModel,Field
from sqlalchemy import Column, Float,Integer,String,Boolean, DateTime
from typing import Optional


class CreateTenantRequest(BaseModel):

    name : str
    natural : bool
    identification_type : int
    identification: int
    num1: str
    num2: str

    contract_id: Optional[int] = None