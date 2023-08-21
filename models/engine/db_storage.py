"""from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine 
from sqlalchemy.orm import sessionmaker
from models.user import User
from models.wallet import Wallet
from models.transaction import Transaction

db_url = "mysql+mysqldb://root:root@localhost/transhub"
engine = create_engine(db_url)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()"""

#!/usr/bin/python3
"""
Contains the class DBStorage
"""

import models
from models.base_model import BaseModel, Base
from models.user import User
from models.wallet import Wallet
from models.transaction import Transaction
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

classes = {"User": User, "Transaction": Transaction, "Wallet": Wallet}


class DBStorage:
    """interaacts with the MySQL database"""
    __engine = None
    __session = None

    def __init__(self):
        """Instantiate a DBStorage object"""
        TRANSHUB_USER = getenv('TRANSHUB_USER')
        TRANSHUB_PWD = getenv('TRANSHUB_PWD')
        TRANSHUB_HOST = getenv('TRANSHUB_HOST')
        TRANSHUB_DB = getenv('TRANSHUB_DB')
        TRANSHUB_ENV = getenv('TRANSHUB_ENV')
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                      format(TRANSHUB_USER,
                                             TRANSHUB_PWD,
                                             TRANSHUB_HOST,
                                             TRANSHUB_DB))
        if TRANSHUB_ENV == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """query on the current database session"""
        new_dict = {}
        for clss in classes:
            if cls is None or cls is classes[clss] or cls is clss:
                objs = self.__session.query(classes[clss]).all()
                for obj in objs:
                    key = obj.__class__.__name__ + '.' + obj.id
                    new_dict[key] = obj
        return (new_dict)

    def new(self, obj):
        """add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """delete from the current database session obj if not None"""
        if obj is not None:
            self.__session.delete(obj)

    def get(self, cls, id):
        """Retrieve one object based on class and its ID."""
        objects = self.__session.query(cls).filter_by(id=id).one()
        return objects if objects else None

    def count(self, cls=None):
        """Count the number of objects in storage matching the given class."""
        return len(self.all(cls))

    def reload(self):
        """reloads data from the database"""
        Base.metadata.create_all(self.__engine)
        sess_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sess_factory)
        self.__session = Session

    def close(self):
        """call remove() method on the private session attribute"""
        self.__session.remove()
