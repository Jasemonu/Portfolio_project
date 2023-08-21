from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Foreignkey
from sqlalchemy.orm import relationship

Base = declarative_base()


class Transaction(Base):
    __tablenaame__ = "transactions"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(120), Foreignkey(user.id))
    wallet_id = Column(String(120), Foreignkey(wallet.id))
    recipient_name = Column(String(120))
    recipient_account = Column(Integer(120))
    amount = Column(Float)
    transaction_type = Column(String(25))
    timestamp = Column(DateTime, default=datetime.utcnow)
    description = Column(String(120))
    status = Column(String)

    user = relationship("User", backref="transaction")
    wallet = relationship("Wallet", backref="transaction")
