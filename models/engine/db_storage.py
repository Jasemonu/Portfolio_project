from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine 
from sqlalchemy.orm import sessionmaker
from models.user import User
from models.wallet import Wallet
from models.transaction import Transaction

db_url = "mysql+mysqldb://root:root@localhost/transhub"
engine = create_engine(db_url)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
