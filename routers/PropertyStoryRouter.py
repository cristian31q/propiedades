from fastapi import  APIRouter , Depends, HTTPException
from Requests import PropertyStroryRequest
from models.PropertyStory import PropertyStory
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
    prefix="/property_story",
    tags=["property_story"]
)

@router.get("/")
def get_all_stories(db: db_dependencies):

    stories = db.query(PropertyStory).all()
    
    if not stories:
        raise HTTPException(status_code=404, detail="No stories found")
    
    return stories

@router.get("/{property_id}")
def get_property_story(property_id:int,db: db_dependencies):

    stories = db.query(PropertyStory).filter(PropertyStory.property_id == property_id ).all()
    
    if not stories:
        raise HTTPException(status_code=404, detail="No property/stories found")
    
    return stories

@router.post("/")
def create_story(story: PropertyStroryRequest.CreatePropertyStory, db: db_dependencies):
    
    
    new_story = PropertyStory(**story.model_dump())

    db.add(new_story)
    db.commit()
    db.refresh(new_story)


    return {"message": "story created successfully", "property_id: ": new_story.property_id}

@router.put("{story_id}")
def update_tenant(story_id: int, tax: PropertyStroryRequest.CreatePropertyStory, db: db_dependencies):
    
    story_db = db.query(PropertyStory).filter(PropertyStory.id == story_id).first()
    
    if not story_db:
        raise HTTPException(status_code=404, detail="tenant not found")
    
    
    for var, value in vars(tax).items():
        if value is not None:
            setattr(story_db, var, value)
    
    
    db.commit()
    db.refresh(story_db)
    
    return story_db

@router.delete("{story_id}")
def delete_tenant(story_id: int, db:db_dependencies):
    
    story_db = db.query(PropertyStory).filter(PropertyStory.id == story_id).first()
    
    if not story_db:
        raise HTTPException(status_code=404, detail="story not found")
    
    
    db.delete(story_db)
    db.commit()
    
    return {"detail": "story deleted successfully"}