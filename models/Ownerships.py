from database import Base
from sqlalchemy import Column, Float,Integer,String,Boolean, ForeignKey
from sqlalchemy.orm import relationship

class Ownerships(Base):
    __tablename__ ='Ownerships'

    id = Column(Integer, primary_key = True, index=True)
    name = Column(String)
    identification_type = Column(Integer)## 0 cedula, 1 pasaporte, 2 nit, 3 otro
    identification = Column(String) 
    person_type = Column(String)
 


