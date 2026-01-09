from database import Base
from sqlalchemy import Column, Float,Integer,String,Boolean, DateTime,ForeignKey
from sqlalchemy.orm import relationship

class Tenants(Base):
    __tablename__ ='Tenants'

    id = Column(Integer, primary_key = True, index=True)
    name = Column(String)
    natural = Column(Boolean)
    identification_type = Column(Integer) ## 0 cedula, 1 pasaporte, 2 nit, 3 otro
    identification = Column(Integer)
    num1 = Column(String,nullable= True)
    num2 = Column(String,nullable= True)
    ################################
    contract_id = Column(Integer)
    # contract = relationship("Contracts",back_populates="Tenants",uselist=False)