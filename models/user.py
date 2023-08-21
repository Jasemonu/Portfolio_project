from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()


class User(Base):
    __tablenaame__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(120), nullable=False)
    last_name = Column(String(120), nullable=False)
    email_address = Column(String(120), unique=True, nullable=False)
    phone_number = Column(Interger(20), nullable=False)
    sex = Column(String(10))
    address = Column(String(120), nullable=False)
    password = Column(String(8, 100), nullable=False, unique=True)
