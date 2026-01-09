from fastapi import  APIRouter , Depends, HTTPException
from Requests import RegistroRequest
from models.Registros import Registros
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
    prefix="/registro",
    tags=["registro"]
)

@router.get("/")
def get_all_registros(db: db_dependencies):

    registro = db.query(Registros).all()
    
    if not registro:
        raise HTTPException(status_code=404, detail="No registros found")
    
    return registro


@router.get("/{registro_id}")
def get_registro(registro_id: int, db: db_dependencies):
    
    registro = db.query(Registros).filter(Registros.id == registro_id).first()
    
    if not registro:
        raise HTTPException(status_code=404, detail="Property not found")
    
    return registro

@router.post("/")
def create_registro(registro: RegistroRequest.CreateRegistroRequest, db: db_dependencies):
    db_registro = Registros(**registro.model_dump())
    db.add(db_registro)
    db.commit()
    db.refresh(db_registro)
    return db_registro

@router.put("{registro_id}")
def update_property(registro_id: int, property: RegistroRequest.CreateRegistroRequest, db: db_dependencies):
    
    registro_db = db.query(Registros).filter(Registros.id == registro_id).first()
    
    if not registro_db:
        raise HTTPException(status_code=404, detail="Registro not found")
    
    
    for var, value in vars(property).items():
        if value is not None:
            setattr(registro_db, var, value)
    
    
    db.commit()
    db.refresh(registro_db)
    
    return registro_db


@router.delete("{registro_id}")
def delete_property(registro_id: int, db:db_dependencies):
    # Obtener la propiedad por ID
    registro_db = db.query(Registros).filter(Registros.id == registro_id).first()
    
    if not registro_db:
        raise HTTPException(status_code=404, detail="Registro not found")
    
    # Eliminar la propiedad
    db.delete(registro_db)
    db.commit()
    
    return {"detail": "Registro deleted successfully"}