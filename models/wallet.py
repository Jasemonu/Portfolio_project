from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Foreignkey
from sqlalchemy.orm import relationship

Base = declarative_base()


class Wallet(Base):
    __tablenaame__ = "wallets"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer(120), Foreignkey("User.id"), nullable=False)
    phone_number = Column(Interger(20), nullable=False)
    pin = Column(Integer(4), nullable=False)
    next_of_kin = Column(String(120))
    next_of_kin_relationnship = Column(String(120))
    next_of_kin_number = Column(Integer(20))

    user = relationship("User", backref="wallets", cascade="all, delete, delete-orphan")
