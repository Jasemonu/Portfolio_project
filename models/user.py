#!/usr/bin/python3
"""user module"""
from models.base_model mport BaseModel, Base
from sqlalchemy import Column, Integer, String


class User(BaseModel, Base):
    """creates user objects"""
    __tablenaame__ = "users"
    first_name = Column(String(120), nullable=False)
    last_name = Column(String(120), nullable=False)
    email_address = Column(String(120), unique=True, nullable=False)
    phone_number = Column(Interger(20), nullable=False)
    sex = Column(String(10))
    address = Column(String(120), nullable=False)
    password = Column(String(8), nullable=False, unique=True)

    def __init__(self, *args, *kwargs):
        """Initializes user"""
        super.__init__(*args, *kwargs)
