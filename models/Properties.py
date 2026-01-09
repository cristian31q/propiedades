from sqlalchemy import Column, Float, Integer, String, Boolean, DateTime, ForeignKey, LargeBinary
from sqlalchemy.orm import relationship
from database import Base

class Properties(Base):
    __tablename__ = 'Properties'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255))
    address = Column(String(255))  
    city = Column(String(100)) 
    neighborhood = Column(String(100))  
    chip = Column(String(100))  
    contract_period = Column(String(50),nullable=True)  
    scripture_date = Column(DateTime)
    scripture_value = Column(Float)
    notaria = Column(String(100))  
    property_status = Column(String)
    property_type = Column(Integer)  # 0 uso propio, 1 vacio, 2 rentado, 3 venta
    
    description = Column(String,nullable = True)

    tax_id = Column(Integer,nullable=True)  
    contract_id = Column(Integer,nullable=True)
    fecha_vacia = Column(DateTime,nullable =True)

    identificador_inmob = Column(String, nullable = True)
    identificador_contadoras =Column(String, nullable =True)

    matricula = Column(String)
    photo = Column(LargeBinary,nullable =True)
    