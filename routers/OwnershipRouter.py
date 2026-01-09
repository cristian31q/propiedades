from fastapi import  APIRouter , Depends, HTTPException
from Requests import OwnershipRequest
from models import Ownerships
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
    prefix="/ownerships",
    tags=["ownerships"]
)

@router.get("/")
def get_all_ownership(db: db_dependencies):
    ownerships = db.query(Ownerships).all()
    
    if not ownerships:
        raise HTTPException(status_code=404, detail="No ownership found")
    
    return ownerships

@router.post("/")
def create_ownership(ownership: OwnershipRequest.CreateOwnershipRequest, db: db_dependencies):
    
    
    new_ownership = Ownerships(**ownership.model_dump())

    db.add(new_ownership)
    db.commit()
    db.refresh(new_ownership)

    return {"message": "Ownership created successfully", "new_ownership_id": new_ownership.id}

@router.put("{ownership_id}")
def update_ownership(ownership_id: int, ownership: OwnershipRequest.CreateOwnershipRequest, db: db_dependencies):
    
    ownership_db = db.query(Ownerships).filter(Ownerships.id == ownership_id).first()
    
    if not ownership_db:
        raise HTTPException(status_code=404, detail="ownership not found")
    
    
    for var, value in vars(ownership).items():
        if value is not None:
            setattr(ownership_db, var, value)
    
    
    db.commit()
    db.refresh(ownership_db)
    
    return ownership_db

@router.delete("{ownership_id}")
def delete_ownership(ownership_id: int, db:db_dependencies):
    
    ownership_db = db.query(Ownerships).filter(Ownerships.id == ownership_id).first()
    
    if not ownership_db:
        raise HTTPException(status_code=404, detail="ownership not found")
    
    
    db.delete(ownership_db)
    db.commit()
    
    return {"detail": "ownership deleted successfully"}