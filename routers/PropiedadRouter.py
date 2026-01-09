from fastapi import  APIRouter , Depends, HTTPException , File, UploadFile
from Requests import PropertiesRequest
from models import Properties , Transactions, Contracts, Ownerships, Taxes, Registros
from models.Registros import Registros
from models.EntityFiles import EntityFiles
from models.ownerproperty import OwnerProperty
from typing import Annotated
from sqlalchemy.orm import Session
from database import engine, sessionlocal
import os
from pathlib import Path
import shutil
import uuid
from fastapi.responses import StreamingResponse
from io import BytesIO


UPLOAD_DIRECTORY = Path("uploads/properties")
UPLOAD_DIRECTORY.mkdir(exist_ok=True)

def getDB():
    db = sessionlocal()
    try:
        yield db
    finally:
        db.close()

db_dependencies = Annotated[Session, Depends(getDB)]

router = APIRouter(
    prefix="/properties",
    tags=["properties"]
)



@router.get("/")
def get_all_properties(db: db_dependencies):
    properties = db.query(Properties).all()
    
    if not properties:
        raise HTTPException(status_code=404, detail="No properties found")
    dto_list = [
        PropertiesRequest.DtoPropertiesRequest(
            id = property.id,
            title=property.title,
            address=property.address,
            city=property.city,
            neighborhood=property.neighborhood,
            chip=property.chip,
            contract_period=property.contract_period,
            scripture_date=property.scripture_date,
            scripture_value=property.scripture_value,
            notaria=property.notaria,
            property_type=property.property_type,
            property_status=property.property_status, 
            tax_id=property.tax_id,  
            contract_id=property.contract_id, 
            description=property.description,
            fecha_vacia=property.fecha_vacia,  
            identificador_contadoras=property.identificador_contadoras,  
            identificador_inmob=property.identificador_inmob,  
            matricula=property.matricula
        )
        for property in properties
    ]
    
    return dto_list

@router.get("/{property_id}")
def get_property_by_id(property_id: int, db: db_dependencies):
    property = db.query(Properties).filter(Properties.id == property_id).first()
    
    if not property:
        raise HTTPException(status_code=404, detail="Property not found")
    

    dto = PropertiesRequest.DtoPropertiesRequest(
            id= property.id,
            title=property.title,
            address=property.address,
            city=property.city,
            neighborhood=property.neighborhood,
            chip=property.chip,
            contract_period=property.contract_period,
            scripture_date=property.scripture_date,
            scripture_value=property.scripture_value,
            notaria=property.notaria,
            property_type=property.property_type,
            property_status=property.property_status,
            tax_id=property.tax_id,
            contract_id=property.contract_id,
            description=property.description,
            fecha_vacia=property.fecha_vacia,
            identificador_contadoras=property.identificador_contadoras,
            identificador_inmob=property.identificador_inmob,
            matricula=property.matricula
    )
    print(dto)

    return dto

@router.get("/{property_id}/transactions")
def get_property_transactions(property_id: int, db: db_dependencies):
    
    property = db.query(Properties).filter(Properties.id == property_id).first()

    if not property:
        raise HTTPException(status_code=404, detail="Property not found")


    transactions = db.query(Transactions).filter(Transactions.property_id == property_id).all()

    if not transactions:
        raise HTTPException(status_code=404, detail="No transactions found for this property")

    return transactions

@router.get("/{property_id}/entities")
def get_entities(property_id: int, db: db_dependencies):
    
    property = db.query(Properties).filter(Properties.id == property_id).first()
    if not property:
        raise HTTPException(status_code=404, detail="Property not found")

  
    entities = db.query(EntityFiles).filter(EntityFiles.property_id == property_id).all()

    if not entities:
        raise HTTPException(status_code=404, detail="No entities found for this property")

    return entities

@router.get("/{property_id}/contracts")
def get_property_contracts(property_id: int, db: db_dependencies):
    
    property = db.query(Properties).filter(Properties.id == property_id).first()
    if not property:
        raise HTTPException(status_code=404, detail="Property not found")


    contracts = db.query(Contracts).filter(Contracts.property_id == property_id).first()

    if not contracts:
        raise HTTPException(status_code=404, detail="No contracts found for this property")

    return contracts

@router.get("/{property_id}/ownerships")
def get_property_ownerships(property_id: int, db: db_dependencies):

    property = db.query(Properties).filter(Properties.id == property_id).first()
    if not property:
        raise HTTPException(status_code=404, detail="Property not found")

    owner_properties = db.query(OwnerProperty).filter(OwnerProperty.Property_id == property.id).all()
    if not owner_properties:
        raise HTTPException(status_code=404, detail="No ownerships found for this property")


    ownership_ids = [op.Owner_id for op in owner_properties]
    ownerships = db.query(Ownerships).filter(Ownerships.id.in_(ownership_ids)).all()

    if not ownerships:
        raise HTTPException(status_code=404, detail="No ownerships found for this property")
    

    ownership_percentage_map = {op.Owner_id: op.percentage for op in owner_properties}


    # Format the response to include each Ownership with the percentage from OwnerProperty
    ownerships_with_percentage = [
        {
            "ownership": ownership,
            "percentage": ownership_percentage_map[ownership.id]
        }
        for ownership in ownerships
    ]

    return ownerships_with_percentage



@router.get("/{property_id}/registros")
def get_registros(property_id: int, db: db_dependencies):
    
    property = db.query(Properties).filter(Properties.id == property_id).first()
    if not property:
        raise HTTPException(status_code=404, detail="Property not found")

  
    registro = db.query(Registros).filter(Registros.property_id == property_id).all()

    if not registro:
        raise HTTPException(status_code=404, detail="No registros found for this property")

    return registro

@router.get("/{property_id}/tax")
def get_property_tax(property_id: int, db: db_dependencies):
    
    property = db.query(Properties).filter(Properties.id == property_id).first()
    if not property:
        raise HTTPException(status_code=404, detail="Property not found")

    
    tax = db.query(Taxes).filter(Taxes.Properties_id == property_id).all()

    if not tax:
        raise HTTPException(status_code=404, detail="No tax found for this property")

    return tax


@router.get("/pending/")
def get_pending_properties(db: db_dependencies):
    properties = db.query(Properties).filter(Properties.photo.is_(None)).all()
    
    if not properties:
        raise HTTPException(status_code=404, detail="No properties found")
    
    return properties

@router.post("/")
def create_property(property: PropertiesRequest.CreatePropertiesRequest, db: db_dependencies):
    db_property = Properties(**property.model_dump())
    db.add(db_property)
    db.commit()
    db.refresh(db_property)
    return db_property

@router.post("/upload/{property_id}")
def upload_photo(property_id:int,tmp_file_type:str,db:db_dependencies,image: UploadFile = File(...)):

    property_db = db.query(Properties).filter(Properties.id == property_id).first()
    if not property_db:
        raise HTTPException(status_code=404, detail="Property not found")
    
    image = image.file.read()

    property_db.photo = image

    db.commit()
    db.refresh(property_db)

    return {"detail": "Image uploaded successfully", "property_id": property_id}




@router.get("/photo/{property_id}")
def get_photo(property_id: int, db:db_dependencies):
    property_db = db.query(Properties).filter(Properties.id == property_id).first()
    if not property_db:
        raise HTTPException(status_code=404, detail="Photo not found")

    # Determine media type dynamically (for example, assume JPEG for now)
    content_type = "image/jpeg"  # Adjust based on your saved content type

    return StreamingResponse(BytesIO(property_db.photo), media_type=content_type)

    

@router.put("{property_id}")
def update_property(property_id: int, property: PropertiesRequest.CreatePropertiesRequest, db: db_dependencies):
    
    property_db = db.query(Properties).filter(Properties.id == property_id).first()
    
    if not property_db:
        raise HTTPException(status_code=404, detail="Property not found")
    
    
    for var, value in vars(property).items():
        if value is not None:
            setattr(property_db, var, value)
    
    
    db.commit()
    db.refresh(property_db)
    
    return property_db

@router.delete("{property_id}")
def delete_property(property_id: int, db:db_dependencies):
    # Obtener la propiedad por ID
    property_db = db.query(Properties).filter(Properties.id == property_id).first()
    
    if not property_db:
        raise HTTPException(status_code=404, detail="Property not found")
    
    # Eliminar la propiedad
    db.delete(property_db)
    db.commit()
    
    return {"detail": "Property deleted successfully"}



