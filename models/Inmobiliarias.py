from database import Base
from sqlalchemy import Column, Float,Integer,String,Boolean, DateTime,ForeignKey
from sqlalchemy.orm import relationship

class Inmobiliarias(Base):
    __tablename__ ='Inmobiliarias'

    id = Column(Integer, primary_key = True, index=True)
    name = Column(String)
    nit = Column(String)
    

    ###########################
    contract_id = Column(Integer,nullable=True)
    
    description = Column(String,nullable=True)
    contact = Column(String,nullable=True)
    contact_phone = Column(String,nullable=True)
    contact_email = Column(String,nullable=True)
    address = Column(String,nullable=True)
    city = Column(String,nullable=True)
    # contract = relationship("Contract",back_populates="Inmbobiliarias",uselist=False)