from database import Base
from sqlalchemy import Column, Float,Integer,String,Boolean, ForeignKey
from sqlalchemy.orm import relationship

class OwnerProperty(Base):
    __tablename__ ='ownerproperty'

    id = Column(Integer, primary_key = True, index=True)
    Owner_id = Column(Integer)
    Property_id = Column(Integer)
    percentage = Column(String) 

 


