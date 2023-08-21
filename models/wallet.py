#!/usr/bin/python3
"""wallet module"""
from models.base_models import BaseModel, Base
from sqlalchemy import Column, Integer, String, Foreignkey
from sqlalchemy.orm import relationship


class Wallet(BaseModel, Base):
    """creates wallet objects"""
    __tablenaame__ = "wallets"
    user_id = Column(Integer(120), Foreignkey("User.id"), nullable=False)
    phone_number = Column(Interger(20), nullable=False)
    pin = Column(Integer(4), nullable=False)
    next_of_kin = Column(String(120))
    next_of_kin_relationnship = Column(String(120))
    next_of_kin_number = Column(Integer(20))

    users = relationship("User", backref="wallets",
                cascade="all, delete, delete-orphan")

    def __init__(self, *args, *kwargs):
        """initializes wallet"""
        super().__init__(*args, *kwargs)
