from database import Base
from sqlalchemy import Column, Float,Integer,String,Boolean, DateTime,ForeignKey, LargeBinary
from sqlalchemy.orm import relationship

class Contracts(Base):
    __tablename__ ='Contracts'

    id = Column(Integer, primary_key = True, index=True)
    canon_arrendamiento = Column(Float)
    administracion = Column(Float)
    begin_date = Column(DateTime)
    renovation_date = Column(DateTime)
    rise = Column(String)
    insurance = Column(Boolean)
    photo = Column(LargeBinary,nullable=True)
    owner_id =Column(Integer, nullable= True)
    ##########################################
    gastos_mtto = Column(Float,nullable=True)
    recibos_domiciliarios = Column(Float,nullable=True)
    extraordinarios = Column(Float,nullable=True)
    comision_admin = Column(Float,nullable=True)
    insurance_canon = Column(Float,nullable=True)
    insurance_admin = Column(Float,nullable=True)
    gastos_varios = Column(Float,nullable=True) 
    ##########################################
    inmobiliaria_id = Column(Integer,nullable=True )
    property_id = Column(Integer)
    months_notify = Column(Integer,nullable = True)
