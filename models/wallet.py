#!/usr/bin/python3
"""wallet module"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship


class Wallet(BaseModel, Base):
    """creates wallet objects"""
    __tablename__ = "wallets"
    user_id = Column(String(120), ForeignKey("users.id"), nullable=True)
    phone_number = Column(Integer, nullable=False)
    pin = Column(Integer, nullable=False)
    next_of_kin = Column(String(120))
    next_of_kin_relationnship = Column(String(120))
    next_of_kin_number = Column(Integer)

    users = relationship("User", back_populates="wallet")
    transactions = relationship('Transaction', back_populates='wallets')

    def __init__(self, *args, **kwargs):
        """initializes wallet"""
        super().__init__(*args, **kwargs)
