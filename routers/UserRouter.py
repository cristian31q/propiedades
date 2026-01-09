from fastapi import  APIRouter , Depends, HTTPException
from Requests import UserRequest
from models import Users
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
    prefix="/users",
    tags=["users"]
)

@router.post("/validate_user/")

def validate_user(login_data: UserRequest.UserLogin, db: db_dependencies):
    
    user = db.query(Users).filter(Users.username == login_data.username).first()


    
    if not user:
        raise HTTPException(status_code=400, detail="username not found")
    
    
    stored_hashed_password = user.hash_password.strip()
    
    
    if not bcrypt.checkpw(login_data.password.encode('utf-8'), stored_hashed_password.encode('utf-8')):
        raise HTTPException(status_code=400, detail="Invalid username or password")
    
    
    return {"message": "User validated successfully", "username": user.username}


@router.post("/")
def create_user(user: UserRequest.UserLogin, db: db_dependencies):
    hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
    new_user = Users(username=user.username, hash_password=hashed_password.decode('utf-8').strip())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User created successfully", "user_id": new_user.id}
