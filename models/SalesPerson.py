from database import Base
from sqlalchemy import Column, Float,Integer,String,Boolean, DateTime,ForeignKey
from sqlalchemy.orm import relationship

class SalesPersons(Base):
    __tablename__ ='Salespersons'

    id = Column(Integer, primary_key = True, index=True)
    name = Column(String)
    identifier = Column(String)
    identifier_type = Column(Integer)
    phone = Column(String)
    
    ###################################
    transaction_id = Column(Integer,nullable=True)
    # transaction = relationship("Transactions",back_populates="Salespersons",uselist=False)
