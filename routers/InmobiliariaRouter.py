from fastapi import  APIRouter , Depends, HTTPException
from Requests import InmobiliariasRequest
from models import Inmobiliarias
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
    prefix="/inmobiliarias",
    tags=["inmobiliarias"]
)

@router.get("/")
def get_all_inmobiliarias(db: db_dependencies):
    inmobiliarias = db.query(Inmobiliarias).all()
    
    if not inmobiliarias:
        raise HTTPException(status_code=404, detail="No inmobiliaria found")
    
    return inmobiliarias

@router.post("/")
def create_inmobiliaria(inmobiliaria: InmobiliariasRequest.CreateInmobiliariaRequest, db: db_dependencies):
    
    
    new_inmobiliaria = Inmobiliarias(**inmobiliaria.model_dump())

    db.add(new_inmobiliaria)
    db.commit()
    db.refresh(new_inmobiliaria)

    return {"message": "Inmobiliaria created successfully", "transaction_id": new_inmobiliaria.id}

@router.put("{inmobiliaria_id}")
def update_inmobiliaria(inmobiliaria_id: int, inmobiliaria: InmobiliariasRequest.CreateInmobiliariaRequest, db: db_dependencies):
    
    inmobiliaria_db = db.query(Inmobiliarias).filter(Inmobiliarias.id == inmobiliaria_id).first()
    
    if not inmobiliaria_db:
        raise HTTPException(status_code=404, detail="Inmobiliaria not found")
    
    
    for var, value in vars(inmobiliaria).items():
        if value is not None:
            setattr(inmobiliaria_db, var, value)
    
    
    db.commit()
    db.refresh(inmobiliaria_db)
    
    return inmobiliaria_db

@router.delete("{inmobiliaria_id}")
def delete_inmobiliaria(inmobiliaria_id: int, db:db_dependencies):
    
    inmobiliaria = db.query(Inmobiliarias).filter(Inmobiliarias.id == inmobiliaria_id).first()
    
    if not inmobiliaria:
        raise HTTPException(status_code=404, detail="Inmobiliaria not found")
    
    
    db.delete(inmobiliaria)
    db.commit()
    
    return {"detail": "inmobiliaria deleted successfully"}