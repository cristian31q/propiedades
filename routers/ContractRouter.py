from fastapi import  APIRouter , Depends, HTTPException, File, UploadFile
from Requests import ContractRequest
from models import Contracts
from typing import Annotated
from sqlalchemy.orm import Session
from database import engine, sessionlocal
from pathlib import Path
import shutil
import uuid
from datetime import datetime, timedelta
from fastapi.responses import StreamingResponse
from io import BytesIO

UPLOAD_DIRECTORY = Path("uploads/contracts")
UPLOAD_DIRECTORY.mkdir(exist_ok=True)


def getDB():
    db = sessionlocal()
    try:
        yield db
    finally:
        db.close()

db_dependencies = Annotated[Session, Depends(getDB)]

router = APIRouter(
    prefix="/contracts",
    tags=["contracts"]
)

@router.get("/")
def get_all_contracts(db: db_dependencies):
    contracts = db.query(Contracts).all()
    
    if not contracts:
        raise HTTPException(status_code=404, detail="No contracts found")
    

    dto_list = [
        ContractRequest.DtoContractRequest(
            id=contract.id,
            canon_arrendamiento=contract.canon_arrendamiento,
            administracion=contract.administracion,
            begin_date=contract.begin_date,
            renovation_date=contract.renovation_date,
            rise=contract.rise,
            insurance=contract.insurance,
            owner_id=contract.owner_id,
            gastos_mtto=contract.gastos_mtto,
            recibos_domiciliarios=contract.recibos_domiciliarios,
            extraordinarios=contract.extraordinarios,
            comision_admin=contract.comision_admin,
            insurance_canon=contract.insurance_canon,
            insurance_admin=contract.insurance_admin,
            gastos_varios=contract.gastos_varios,
            inmobiliaria_id=contract.inmobiliaria_id,
            property_id=contract.property_id,
            months_notify=contract.months_notify
        )
        for contract in contracts
    ]
    return dto_list
    
@router.get("/{property_id}")
def get_contract(property_id: int,db: db_dependencies):
    contract = db.query(Contracts).filter(Contracts.property_id == property_id).first()
    
    if not contract:
        raise HTTPException(status_code=404, detail="No contract found")
    

    dto_list = [
        ContractRequest.DtoContractRequest(
            id=contract.id,
            canon_arrendamiento=contract.canon_arrendamiento,
            administracion=contract.administracion,
            begin_date=contract.begin_date,
            renovation_date=contract.renovation_date,
            rise=contract.rise,
            insurance=contract.insurance,
            owner_id=contract.owner_id,
            gastos_mtto=contract.gastos_mtto,
            recibos_domiciliarios=contract.recibos_domiciliarios,
            extraordinarios=contract.extraordinarios,
            comision_admin=contract.comision_admin,
            insurance_canon=contract.insurance_canon,
            insurance_admin=contract.insurance_admin,
            gastos_varios=contract.gastos_varios,
            inmobiliaria_id=contract.inmobiliaria_id,
            property_id=contract.property_id,
            months_notify=contract.months_notify
        )
        
    ]
    return dto_list

@router.get("/pending/")
def get_pending_contracts(db: db_dependencies):
    contract = db.query(Contracts).filter(Contracts.url_contract.is_(None)).all()
    
    if not contract:
        raise HTTPException(status_code=404, detail="No contracts found")
    
    return contract

@router.get("/about_to_renovate")
def get_contracts_renovation(db: db_dependencies):
 
    today = datetime.today()
    
    contracts = db.query(Contracts).filter(
        Contracts.renovation_date.between(today, contracts.months_notify)
    ).all()

    if not contracts:
        raise HTTPException(status_code=404, detail="No contracts with renovation date in the next 3 months found")
    
    return contracts

@router.post("/")
def create_contract(contract: ContractRequest.CreateContractRequest, db: db_dependencies):
    
    
    new_contract = Contracts(**contract.model_dump())

    db.add(new_contract)
    db.commit()
    db.refresh(new_contract)

    return {"message": "new_contract created successfully", "transaction_id": new_contract.id}

@router.post("/upload/{contract_id}")
def upload_photo(contract_id:int,db:db_dependencies,image: UploadFile = File(...)):

    contract_db = db.query(Contracts).filter(Contracts.id == contract_id).first()
    if not contract_db:
        raise HTTPException(status_code=404, detail="contract not found")
    
    # Read the image content as binary
    image = image.file.read()

    contract_db.photo = image

    db.commit()
    db.refresh(contract_db)

    return {"detail": "Image uploaded successfully", "contract_id": contract_db.id}


@router.get("/photo/{contract_id}")
def get_photo(contract_id: int, db:db_dependencies):
    contract  = db.query(Contracts).filter(Contracts.id == contract_id).first()
    if not contract or not contract.photo:
        raise HTTPException(status_code=404, detail="Photo not found")

    content_type = "image/jpeg"  

    return StreamingResponse(BytesIO(contract.photo), media_type=content_type)

@router.put("{contract_id}")
def update_contract(contract_id: int, contract: ContractRequest.CreateContractRequest, db: db_dependencies):
    
    contract_db = db.query(Contracts).filter(Contracts.id == contract_id).first()
    
    if not contract_db:
        raise HTTPException(status_code=404, detail="Contract not found")
    
    
    for var, value in vars(contract).items():
        if value is not None:
            setattr(contract_db, var, value)
    
    
    db.commit()
    db.refresh(contract_db)
    
    return contract_db

@router.delete("{contract_id}")
def delete_contract(contract_id: int, db:db_dependencies):
    
    contract_db = db.query(Contracts).filter(Contracts.id == contract_id).first()
    
    if not contract_db:
        raise HTTPException(status_code=404, detail="Contract not found")
    
    
    db.delete(contract_db)
    db.commit()
    
    return {"detail": "Contract deleted successfully"}



    
