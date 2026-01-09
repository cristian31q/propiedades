from fastapi import  APIRouter , Depends, HTTPException
from Requests import TenantRequest
from models import Tenants, Contracts
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
    prefix="/tenants",
    tags=["tenants"]
)

@router.get("/")
def get_all_tenants(db: db_dependencies):

    tenants = db.query(Tenants).all()
    
    if not tenants:
        raise HTTPException(status_code=404, detail="No tenant found")
    
    return tenants

@router.get("/{contract_id}")
def get_tenant(contract_id:int,db: db_dependencies):

    tenant = db.query(Tenants).filter(Contracts.id == contract_id).first()
    
    if not tenant:
        raise HTTPException(status_code=404, detail="No tenant found")
    
    return tenant

@router.post("/")
def create_tenant(tenant: TenantRequest.CreateTenantRequest, db: db_dependencies):
    
    
    new_tenant = Tenants(**tenant.model_dump())

    db.add(new_tenant)
    db.commit()
    db.refresh(new_tenant)


    return {"message": "tenant created successfully", "tenant_id: ": new_tenant.id}

@router.put("{tenant_id}")
def update_tenant(tenant_id: int, tax: TenantRequest.CreateTenantRequest, db: db_dependencies):
    
    tenant_db = db.query(Tenants).filter(Tenants.id == tenant_id).first()
    
    if not tenant_db:
        raise HTTPException(status_code=404, detail="tenant not found")
    
    
    for var, value in vars(tax).items():
        if value is not None:
            setattr(tenant_db, var, value)
    
    
    db.commit()
    db.refresh(tenant_db)
    
    return tenant_db

@router.delete("{tenant_id}")
def delete_tenant(tenant_id: int, db:db_dependencies):
    
    tenant_db = db.query(Tenants).filter(Tenants.id == tenant_id).first()
    
    if not tenant_db:
        raise HTTPException(status_code=404, detail="Tenant not found")
    
    
    db.delete(tenant_db)
    db.commit()
    
    return {"detail": "tenant deleted successfully"}