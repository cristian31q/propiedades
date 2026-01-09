from database import Base
from sqlalchemy import Column, Float,Integer,String,Boolean, DateTime,ForeignKey, LargeBinary
from sqlalchemy.orm import relationship

class EntityFiles(Base):
    __tablename__ ='entity_files'

    id = Column(Integer, primary_key = True, index=True)
    photo = Column(LargeBinary,nullable=True)
    file_type =Column(String)
    property_id =Column(Integer)