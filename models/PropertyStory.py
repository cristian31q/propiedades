from database import Base
from sqlalchemy import Column, Float,Integer,String,Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship

class PropertyStory(Base):
    __tablename__ ='PropertyStory'

    id = Column(Integer, primary_key = True, index=True)
    property_id = Column(Integer)
    tipo = Column(String)## 0 cedula, 1 pasaporte, 2 nit, 3 otro
    fecha_inicio = Column(DateTime) 
    fecha_fin = Column(DateTime)
    description = Column(String)
 


