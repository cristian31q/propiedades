from sqlalchemy import Column, Float, Integer, String, DateTime, ForeignKey, LargeBinary
from sqlalchemy.orm import relationship
from database import Base

class Taxes(Base):
    __tablename__ = 'Taxes'

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String)
    tax_year = Column(DateTime)
    avaluo = Column(Float)
    photo = Column(LargeBinary,nullable = True)
    payment_day = Column(DateTime)
    account_num = Column(String)

    Properties_id = Column(Integer,nullable=True)
    value = Column(Float)
    forma_pago = Column(String)
    