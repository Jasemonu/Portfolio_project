#!/usr/bin/python3
"""user module"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from flask_login import UserMixin


class User(BaseModel, UserMixin, Base):
    """creates user objects"""
    __tablename__ = "users"
    first_name = Column(String(120), nullable=False)
    last_name = Column(String(120), nullable=False)
    email_address = Column(String(120), unique=True, nullable=False)
    phone_number = Column(String(15), nullable=False)
    sex = Column(String(10))
    address = Column(String(120), nullable=False)
    password = Column(String(120), nullable=False)
    wallet = relationship('Wallet', back_populates='user',
                          cascade='all, delete')
    transactions = relationship('Transaction', back_populates='user',
                                cascade='all, delete')

    def __init__(self, *args, **kwargs):
        """Initializes user"""
        super().__init__(*args, **kwargs)
