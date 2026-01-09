from pydantic import BaseModel,Field
from sqlalchemy import Column, Float,Integer,String,Boolean, DateTime


class CreateSalesPersonRequest(BaseModel):

    name : str
    identifier: str
    identifier_type: int
    phone: str

    transaction_id: int