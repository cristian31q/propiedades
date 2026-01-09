from pydantic import BaseModel,Field
from typing import Optional

class CreateOwnerPropertyRequest(BaseModel):

    Owner_id: int
    Property_id: int
    percentage: float