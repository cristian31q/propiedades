from fastapi import  APIRouter , Depends, HTTPException, File, UploadFile
from Requests import TransactionsRequest
from models import Transactions,Properties
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
    prefix="/transactions",
    tags=["transactions"]
)
@router.get("/")
def get_all_transactions(db: db_dependencies):

    transactions = db.query(Transactions).all()
    
    if not transactions:
        raise HTTPException(status_code=404, detail="No transaction found")
    
    dto_list = [
        TransactionsRequest.DtoTenantRequest(
            id = transaction.id,
            transaction_state=transaction.transaction_state,
            transaction_type=transaction.transaction_type,
            value=transaction.value,
            income=transaction.income,
            account_num=transaction.account_num,
            property_id=transaction.property_id,
            salesperson_id=transaction.salesperson_id,
            efectivo=transaction.efectivo,
            transferencia=transaction.transferencia,
            permuta=transaction.permuta
        )
        for transaction in transactions
    ]
    
    return dto_list

@router.get("/{property_id}")
def get_transaction(property_id:int,db: db_dependencies):

    transactions = db.query(Transactions).filter(Transactions.property_id == property_id).all()
    
    if not transactions:
        raise HTTPException(status_code=404, detail="No transaction found")
    
    dto_list = [
        TransactionsRequest.DtoTenantRequest(
            id=transaction.id,
            transaction_state=transaction.transaction_state,
            transaction_type=transaction.transaction_type,
            value=transaction.value,
            income=transaction.income,
            account_num=transaction.account_num,
            property_id=transaction.property_id,
            salesperson_id=transaction.salesperson_id,
            efectivo=transaction.efectivo,
            transferencia=transaction.transferencia,
            permuta=transaction.permuta
        )
        for transaction in transactions
    ]
    
    return dto_list

@router.post("/")
def create_transaction(transaction: TransactionsRequest.CreateTenantRequest, db: db_dependencies):
    
    new_transaction = Transactions(**transaction.model_dump())

    db.add(new_transaction)
    db.commit()
    db.refresh(new_transaction)

    return {"message": "Transaction created successfully", "transaction_id": new_transaction.id}

@router.post("upload/{transaction_id}")
def upload_contract(transaction_id:int, db:db_dependencies,image: UploadFile = File(...)):

    transaction_db = db.query(Transactions).filter(Transactions.id == transaction_id).first()
    
    if not transaction_db:
        raise HTTPException(status_code=404, detail="transaction not found")
    
    unique_filename = f"{uuid.uuid4()}_{image.filename}"
    image_path = UPLOAD_DIRECTORY / unique_filename

    # Guardar la imagen en el servidor
    with image_path.open("wb") as buffer:
        shutil.copyfileobj(image.file, buffer)

    # Actualizar el registro de la propiedad con la ruta de la imagen
    transaction_db.url_contract = str(image_path)
    db.commit()
    db.refresh(transaction_db)

    return {"detail": "Image uploaded successfully", "image_path": str(transaction_db.url_contract)}
    

@router.put("{transaction_id}")
def update_transaction(transaction_id: int, transaction: TransactionsRequest.CreateTenantRequest, db: db_dependencies):
    
    transaction_db = db.query(transaction_id).filter(Transactions.id == transaction_id).first()
    
    if not transaction_db:
        raise HTTPException(status_code=404, detail="transaction not found")
    
    
    for var, value in vars(transaction).items():
        if value is not None:
            setattr(transaction_db, var, value)
    
    
    db.commit()
    db.refresh(transaction_db)
    
    return transaction_db

@router.post("/upload/{transaction_id}")
def upload_photo(transaction_id:int, db:db_dependencies,image: UploadFile = File(...)):

    transaction_db = db.query(Transactions).filter(Transactions.id == transaction_id).first()
    if not transaction_db:
        raise HTTPException(status_code=404, detail="Property not found")
    
    # Read the image content as binary
    image_data = image.file.read()
    
    # Update the `photo` field in the property record
    transaction_db.photo = image_data
    db.commit()
    db.refresh(transaction_db)

    return {"detail": "Image uploaded successfully", "property_id": transaction_id}


@router.get("/photo/{transaction_id}")
def get_photo(property_id: int, db:db_dependencies):
    transaction_id_db = db.query(Transactions).filter(Transactions.id == property_id).first()
    if not transaction_id_db or not transaction_id_db.photo:
        raise HTTPException(status_code=404, detail="Photo not found")

    # Determine media type dynamically (for example, assume JPEG for now)
    content_type = "image/jpeg"  # Adjust based on your saved content type

    return StreamingResponse(BytesIO(transaction_id_db.photo), media_type=content_type)


@router.delete("{transaction_id}")
def delete_transaction(transaction_id: int, db:db_dependencies):
    
    transaction_db = db.query(Transactions).filter(Transactions.id == transaction_id).first()
    
    if not transaction_db:
        raise HTTPException(status_code=404, detail="transaction not found")
    
    
    db.delete(transaction_db)
    db.commit()
    
    return {"detail": "transaction deleted successfully"}


