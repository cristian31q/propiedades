from database import Base
from sqlalchemy import Column, Float,Integer,String,Boolean, DateTime,ForeignKey, LargeBinary
from sqlalchemy.orm import relationship

class Transactions(Base):
    __tablename__ ='Transactions'

    id = Column(Integer, primary_key = True, index=True)
    transaction_state = Column(Integer,nullable =True) ## 0 arrendamiento, 1 venta,  2 tax?
    value = Column(Float)
    income = Column(Boolean) ## true si es ingreso, false si es un gasto
    account_num = Column(String)
    transaction_type = Column(String) ## 0 efectivo, 1 transferencia, 2 cheque, 3 inmobiliaria
    photo = Column(LargeBinary,nullable=True)  
    #######################################
    salesperson_id = Column(Integer,nullable=True)
    property_id = Column(Integer,nullable=True)
    efectivo = Column(Float, nullable = True)
    transferencia = Column(Float,nullable=True)
    permuta = Column(Float,nullable=True)
