from database import Base
from sqlalchemy import Column, Integer,String,Boolean, ForeignKey

class Users(Base):
    __tablename__ ='users'

    id = Column(Integer, primary_key = True, index=True)
    username = Column(String)
    email = Column(String)
    hash_password = Column(String)
    admin = Column(String)
    first_name = Column(String)
    lastaname = Column(String)
    is_active = Column(Boolean, default = False)


