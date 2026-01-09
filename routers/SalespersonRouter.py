from fastapi import  APIRouter , Depends, HTTPException
from Requests import SalesPersonRequest
from models import SalesPersons
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
    prefix="/salesperson",
    tags=["salesperson"]
)

@router.get("/")
def get_all_salesperson(db: db_dependencies):

    salesperson = db.query(SalesPersons).all()
    
    if not salesperson:
        raise HTTPException(status_code=404, detail="No salesperson found")
    
    return salesperson

@router.post("/")
def create_salesperson(salesperson: SalesPersonRequest.CreateSalesPersonRequest, db: db_dependencies):
    
    
    new_salesperson = SalesPersons(**salesperson.model_dump())

    db.add(new_salesperson)
    db.commit()
    db.refresh(new_salesperson)


    return {"message": "salesperson created successfully", "sales_person: id": new_salesperson.id}

@router.put("{salesperson_id}")
def update_salesperson(salesperson_id: int, salesperson: SalesPersonRequest.CreateSalesPersonRequest, db: db_dependencies):
    
    salesperson_db = db.query(SalesPersons).filter(SalesPersons.id == salesperson_id).first()
    
    if not salesperson_db:
        raise HTTPException(status_code=404, detail="Salesperson not found")
    
    
    for var, value in vars(salesperson).items():
        if value is not None:
            setattr(salesperson_db, var, value)
    
    
    db.commit()
    db.refresh(salesperson_db)
    
    return salesperson_db

@router.delete("{salesperson_id}")
def delete_salesperson(salesperson_id: int, db:db_dependencies):
    
    salesperson_db = db.query(SalesPersons).filter(SalesPersons.id == salesperson_id).first()
    
    if not salesperson_db:
        raise HTTPException(status_code=404, detail="Salesperson not found")
    
    
    db.delete(salesperson_db)
    db.commit()
    
    return {"detail": "salesperson deleted successfully"}