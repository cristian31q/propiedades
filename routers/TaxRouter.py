from fastapi import  APIRouter , Depends, HTTPException, File, UploadFile
from Requests import TaxRequest
from models import Taxes
from typing import Annotated
from sqlalchemy.orm import Session
from database import engine, sessionlocal
from pathlib import Path
import shutil
import uuid
from fastapi.responses import StreamingResponse
from io import BytesIO

UPLOAD_DIRECTORY = Path("uploads/transactions")
UPLOAD_DIRECTORY.mkdir(exist_ok=True)

def getDB():
    db = sessionlocal()
    try:
        yield db
    finally:
        db.close()

db_dependencies = Annotated[Session, Depends(getDB)]

router = APIRouter(
    prefix="/taxes",
    tags=["taxes"]
)

@router.get("/")
def get_all_taxes(db: db_dependencies):

    taxes = db.query(Taxes).all()
    
    if not taxes:
        raise HTTPException(status_code=404, detail="No taxes found")
    

    dto_list = [
        TaxRequest.DtoTaxRequest(
            id=tax.id,
            description=tax.description,
            tax_year=tax.tax_year,
            avaluo=tax.avaluo,
            payment_day=tax.payment_day,
            account_num=tax.account_num,
            Properties_id=tax.Properties_id,
            value=tax.value,
            forma_pago=tax.forma_pago
        )
        for tax in taxes
    ]

    return dto_list


@router.get("/{property_id}")
def get_tax(property_id: int,db: db_dependencies):

    tax = db.query(Taxes).filter(Taxes.Properties_id == property_id).first()
    
    if not tax:
        raise HTTPException(status_code=404, detail="No taxes found")
    

    dto_list = [
        TaxRequest.DtoTaxRequest(
            id=tax.id,
            description=tax.description,
            tax_year=tax.tax_year,
            avaluo=tax.avaluo,
            payment_day=tax.payment_day,
            account_num=tax.account_num,
            Properties_id=tax.Properties_id,
            value=tax.value,
            forma_pago=tax.forma_pago
        )
    ]

    return dto_list

@router.post("/upload/{tax_id}")
def upload_photo(tax_id:int,db:db_dependencies,image: UploadFile = File(...)):

    tax_db = db.query(Taxes).filter(Taxes.id == tax_id).first()
    if not tax_db:
        raise HTTPException(status_code=404, detail="contract not found")
    
    # Read the image content as binary
    image = image.file.read()

    tax_db.photo = image

    db.commit()
    db.refresh(tax_db)

    return {"detail": "Image uploaded successfully", "tax_id": tax_db.id}


@router.get("/photo/{tax_id}")
def get_photo(tax_id: int, db:db_dependencies):
    tax  = db.query(Taxes).filter(Taxes.id == tax_id).first()
    if not tax or not tax.photo:
        raise HTTPException(status_code=404, detail="Photo not found")

    content_type = "image/jpeg"  

    return StreamingResponse(BytesIO(tax.photo), media_type=content_type)

@router.post("/")
def create_tax(tax: TaxRequest.CreateTaxRequest, db: db_dependencies):
    
    
    new_tax = Taxes(**tax.model_dump())

    db.add(new_tax)
    db.commit()
    db.refresh(new_tax)


    return {"message": "taxed created successfully", "tax_id: ": new_tax.id}

@router.put("{tax_id}")
def update_tax(tax_id: int, tax: TaxRequest.CreateTaxRequest, db: db_dependencies):
    
    tax_db = db.query(Taxes).filter(Taxes.id == tax_id).first()
    
    if not tax_db:
        raise HTTPException(status_code=404, detail="tax not found")
    
    
    for var, value in vars(tax).items():
        if value is not None:
            setattr(tax_db, var, value)
    
    
    db.commit()
    db.refresh(tax_db)
    
    return tax_db

@router.delete("{tax_id}")
def delete_tax(tax_id: int, db:db_dependencies):
    
    tax_db = db.query(Taxes).filter(Taxes.id == tax_id).first()
    
    if not tax_db:
        raise HTTPException(status_code=404, detail="Tax not found")
    
    
    db.delete(tax_db)
    db.commit()
    
    return {"detail": "tax deleted successfully"}

@router.post("upload/{tax_id}")
def upload_transaction(tax_id:int, db:db_dependencies,image: UploadFile = File(...)):

    tax_db = db.query(Taxes).filter(Taxes.id == tax_id).first()
    
    if not tax_db:
        raise HTTPException(status_code=404, detail="Contract not found")
    
    unique_filename = f"{uuid.uuid4()}_{image.filename}"
    image_path = UPLOAD_DIRECTORY / unique_filename

    # Guardar la imagen en el servidor
    with image_path.open("wb") as buffer:
        shutil.copyfileobj(image.file, buffer)

    # Actualizar el registro de la propiedad con la ruta de la imagen
    tax_db.url_proof = str(image_path)
    db.commit()
    db.refresh(tax_db)

    return {"detail": "Image uploaded successfully", "image_path": str(tax_db.url_proof)}
    
