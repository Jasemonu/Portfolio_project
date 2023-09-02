#!/usr/bin/python3
"""transaction module"""

from models.base_model import BaseModel, Base
from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship
from sqlalchemy import DateTime
from datetime import datetime


class Transaction(BaseModel, Base):
    """Class for transactions objects"""
    __tablename__ = "transactions"
    user_id = Column(String(120), ForeignKey('users.id'))
    wallet_id = Column(String(120), ForeignKey('wallets.id'))
    recipient_name = Column(String(120))
    recipient_account = Column(Integer)
    amount = Column(Float)
    transaction_type = Column(String(25))
    timestamp = Column(DateTime, default=datetime.utcnow)
    description = Column(String(120))
    status = Column(String(20))

    user = relationship("User", back_populates="transactions")
    wallet = relationship("Wallet", back_populates="transactions")

    def __init__(self, *args, **kwargs):
        """initializes transaction"""
        super().__init__(*args, **kwargs)
