from pydantic import BaseModel,Field
from typing import Optional

class CreateOwnershipRequest(BaseModel):

    name : str
    identification_type: int
    identification: str
    person_type : Optional[str] = None