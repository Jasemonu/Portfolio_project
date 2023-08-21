#!/usr/bin/python3
"""transaction module"""

from models.base_model import BaseModel, Base
from sqlalchemy import Column, Integer, String, Foreignkey
from sqlalchemy.orm import relationship


class Transaction(BaseModel, Base):
    __tablenaame__ = "transactions"
    user_id = Column(String(120), Foreignkey('user.id'))
    wallet_id = Column(String(120), Foreignkey('wallet.id'))
    recipient_name = Column(String(120))
    recipient_account = Column(Integer(120))
    amount = Column(Float)
    transaction_type = Column(String(25))
    timestamp = Column(DateTime, default=datetime.utcnow)
    description = Column(String(120))
    status = Column(String)

    users = relationship("User", backref="transaction")
    wallets = relationship("Wallet", backref="transaction")

    def __init__(self, *args, *kwargs):
        """initializes transaction"""
        super().__init__(*args, *kwargs)
