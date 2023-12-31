#!/usr/bin/python3
"""wallet module"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship


class Wallet(BaseModel, Base):
    """creates wallet objects"""
    __tablename__ = "wallets"
    user_id = Column(String(120), ForeignKey("users.id"), nullable=True)
    phone_number = Column(String(15), nullable=False)
    pin = Column(Integer, nullable=False)
    next_of_kin = Column(String(120))
    next_of_kin_relationship = Column(String(120))
    next_of_kin_number = Column(String(15))
    balance = Column(Float, default=0.00)
    user = relationship("User", back_populates="wallet")
    transactions = relationship('Transaction', back_populates='wallet',
                                cascade='all, delete')

    def __init__(self, *args, **kwargs):
        """initializes wallet"""
        super().__init__(*args, **kwargs)
