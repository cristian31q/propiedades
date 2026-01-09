from database import Base
from sqlalchemy import Column, Float,Integer,String,Boolean, DateTime,ForeignKey,JSON
from sqlalchemy.orm import relationship

class Registros(Base):
    __tablename__ ='Registros'

    id = Column(Integer, primary_key = True, index=True)
    my_json = Column(JSON)
    total = Column(Float)
    fechaInicio = Column(DateTime)
    fechaCorte = Column(DateTime)
    property_id = Column(Integer)