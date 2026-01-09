from pydantic import BaseModel,Field
from typing import Optional

class CreateInmobiliariaRequest(BaseModel):

    name : str
    nit : str

    contract_id : Optional[int] = None

    description: Optional[str] = None
    contact: Optional[str] = None
    contact_phone: Optional[str] = None
    contact_email: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
