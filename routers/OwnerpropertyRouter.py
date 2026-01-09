from fastapi import  APIRouter , Depends, HTTPException
from Requests import ownerpropertyRequest
from models.ownerproperty import OwnerProperty
from typing import Annotated
from sqlalchemy.orm import Session
from database import engine, sessionlocal
import bcrypt

def getDB():
    db = sessionlocal()
    try:
        yield db
    finally:
        db.close()

db_dependencies = Annotated[Session, Depends(getDB)]

router = APIRouter(
    prefix="/owner_property",
    tags=["owner_property"]
)

@router.get("/")
def get_links(db: db_dependencies):
    link = db.query(OwnerProperty).all()
    
    if not link:
        raise HTTPException(status_code=404, detail="No contracts found")
    
    return link

@router.post("/")
def linking(link: ownerpropertyRequest.CreateOwnerPropertyRequest, db: db_dependencies):
    
    link = OwnerProperty(**link.model_dump())

    db.add(link)
    db.commit()
    db.refresh(link)

    return {"message": "linked successfully"}



@router.put("/")
def update_link(OwnerProperty_id:int,OwnerProperty_tmp: ownerpropertyRequest.CreateOwnerPropertyRequest, db: db_dependencies):

    OwnerProperty_db = db.query(OwnerProperty).filter(OwnerProperty.id == OwnerProperty_id).first()

    if not OwnerProperty_db:
        raise HTTPException(status_code=404, detail="Contract not found")
    
    for var, value in vars(OwnerProperty_tmp).items():
        if value is not None:
            setattr(OwnerProperty_db, var, value)
    
    
    db.commit()
    db.refresh(OwnerProperty_db)
    
    return OwnerProperty_db

@router.delete("{ownerprop_id}")
def delete_ownerproperty(ownerprop_id: int, db:db_dependencies):
    # Obtener la propiedad por ID
    ownerprop_db = db.query(OwnerProperty).filter(OwnerProperty.id == ownerprop_id).first()
    
    if not ownerprop_db:
        raise HTTPException(status_code=404, detail="Property not found")
    
    # Eliminar la propiedad
    db.delete(ownerprop_db)
    db.commit()
    
    return {"detail": "ownerprop_db deleted successfully"}
    
