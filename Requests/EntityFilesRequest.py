from pydantic import BaseModel,Field
from sqlalchemy import DateTime
from typing import Optional
from datetime import datetime

class CreateEntityFileRequest(BaseModel):

    property_id:int
    file_type:str

class DtoEntityFileRequest(BaseModel):
    id: int
    property_id:int
    file_type:str

