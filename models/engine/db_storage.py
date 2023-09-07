#!/usr/bin/python3
"""
Contains the class DBStorage
"""

import models
from os import getenv
from models.base_model import BaseModel, Base
from models.user import User
from models.wallet import Wallet
from models.transaction import Transaction
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import datetime

classes = {"User": User, "Transaction": Transaction, "Wallet": Wallet}


class DBStorage:
    """interaacts with the MySQL database"""
    __engine = None
    __session = None

    def __init__(self):
        """Instantiate a DBStorage object"""
        TRANSHUB_USER = getenv('TRANSHUB_USER')
        if not TRANSHUB_USER:
            TRANSHUB_USER = 'root'
        TRANSHUB_PWD = getenv('TRANSHUB_PWD')
        if not TRANSHUB_PWD:
            TRANSHUB_PWD = 'root'
        TRANSHUB_HOST = getenv('TRANSHUB_HOST')
        if not TRANSHUB_HOST:
            TRANSHUB_HOST = 'localhost'
        TRANSHUB_DB = getenv('TRANSHUB_DB')
        if not TRANSHUB_DB:
            TRANSHUB_DB = 'transhub'
        TRANSHUB_ENV = getenv('TRANSHUB_ENV')
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                      format(TRANSHUB_USER,
                                             TRANSHUB_PWD,
                                             TRANSHUB_HOST,
                                             TRANSHUB_DB))
        if TRANSHUB_ENV == "test":
            Base.metadata.drop_all(self.__engine)
            self.__session = scoped_session(sessionmaker(bind=self.__engine))

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
        """Retrieve one object based on class and its id"""
        objects = self.__session.query(cls).filter_by(id=id).first()
        return objects if objects else None

    def get_email(self, cls, email_address):
        """Retrieve one object based on class and its email"""
        objects = self.__session.query(cls).filter_by(
                    email_address=email_address).first()
        return objects if objects else None

    def wallet(self, cls, acnt):
        """Retrieve one wallet object based on class and its account"""
        objects = self.__session.query(cls).filter_by(
                    phone_number=acnt).first()
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

    def update(self, obj, items):
        """Updates table attributes in database"""
        for key, value in items.items():
            setattr(obj, key, value)
        obj.save()
        return obj

    def close(self):
        """call remove() method on the private session attribute"""
        self.__session.close()
