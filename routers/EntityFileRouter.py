from fastapi import  APIRouter , Depends, HTTPException, File, UploadFile
from Requests import EntityFilesRequest
from models.EntityFiles import EntityFiles
from models.Properties import Properties
from typing import Annotated
from sqlalchemy.orm import Session
from database import engine, sessionlocal
from pathlib import Path
import shutil
import uuid
from datetime import datetime, timedelta
from pydantic import BaseModel
from fastapi.responses import StreamingResponse
from io import BytesIO

UPLOAD_DIRECTORY = Path("uploads/entity_files")
UPLOAD_DIRECTORY.mkdir(exist_ok=True)


def getDB():
    db = sessionlocal()
    try:
        yield db
    finally:
        db.close()

db_dependencies = Annotated[Session, Depends(getDB)]

router = APIRouter(
    prefix="/entity_files",
    tags=["entity_files"]
)


@router.get("/")
def get_entity_files(db: db_dependencies):
    entity_files = db.query(EntityFiles).all()
    
    if not entity_files:
        raise HTTPException(status_code=404, detail="No entity_files found")
    
    dtos = []

    for entity in entity_files:
        dto = EntityFilesRequest.DtoEntityFileRequest(
        id= entity.id,
        property_id=entity.property_id,
        file_type=entity.file_type  
        )

        dtos.append(dto)
    
    return dtos


@router.get("/{property_id}")
def get_entity_files(property_id:int,db: db_dependencies):


    property_db = db.query(Properties).filter(Properties.id == property_id).first()
    if not property_db:
        raise HTTPException(status_code=404, detail="Property not found")
    

    entity_files = db.query(EntityFiles).filter(EntityFiles.property_id == property_id).all()
    print("alo2")
    if not entity_files:
        raise HTTPException(status_code=404, detail="No entity_files found")

    dtos = []

    for entity in entity_files:
        dto = CreateEntityFileRequest(
        property_id=property_db.id,
        file_type=entity.file_type  
        )

        dtos.append(dto)
    
    return dtos

class CreateEntityFileRequest(BaseModel):
    property_id: int
    file_type: str


@router.post("/upload/{property_id}")
def upload_photo(property_id:int,tmp_file_type:str,db:db_dependencies,image: UploadFile = File(...)):

    property_db = db.query(Properties).filter(Properties.id == property_id).first()
    if not property_db:
        raise HTTPException(status_code=404, detail="Property not found")
    
    # Read the image content as binary
    image = image.file.read()

    new_entity = EntityFiles(
        photo = image,
        file_type = tmp_file_type,
        property_id = property_id
    )

    db.add(new_entity)
    db.commit()
    db.refresh(new_entity)

    return {"detail": "Image uploaded successfully", "property_id": property_id}


@router.get("/photo/{file_id}")
def get_photo_binary(file_id: int, db: db_dependencies):
    entity_file = db.query(EntityFiles).filter(EntityFiles.id == file_id).first()
    if not entity_file or not entity_file.photo:
        raise HTTPException(status_code=404, detail="Photo not found")
    
    # Adjust media_type based on stored image format if needed
    return StreamingResponse(BytesIO(entity_file.photo), media_type="image/jpeg")


@router.delete("{entity_id}")
def delete_entity(entity_id: int, db:db_dependencies):
    
    entity_db = db.query(EntityFiles).filter(EntityFiles.id == entity_id).first()
    
    if not entity_db:
        raise HTTPException(status_code=404, detail="entity_id not found")
    
    
    db.delete(entity_db)
    db.commit()
    
    return {"detail": "entity_id deleted successfully"}
