# encoding=utf-8
from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, create_engine, DateTime, Float, Unicode
from sqlalchemy.dialects.postgresql import JSON, ARRAY, INTERVAL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.mutable import MutableDict
from datetime import datetime


class ObjectDict(dict):
    """Makes a dictionary behave like an object, with attribute-style access.
    """

    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)

    def __setattr__(self, name, value):
        self[name] = value

# 创建对象的基类:
Base = declarative_base()

def to_dict(self):
    result = ObjectDict()
    for c in self.__table__.columns:
        value = getattr(self, c.name, None)
        if isinstance(c.type, DateTime):
            if value:
                if type(value) != unicode:
                    result[c.name] = value.strftime("%Y-%m-%d %H:%M:%S")
                else:
                    result[c.name] = value
            else:
                result[c.name] = value
        elif isinstance(c.type, Float):
            if value:
                result[c.name] = float(value)
            else:
                result[c.name] = value
        else:
            result[c.name] = value
    return result
 
Base.to_dict = to_dict


class SetOfBook(Base):
    __tablename__ = 'set_of_books'

    id = Column(Integer, primary_key=True)
    set_of_book = Column(Unicode(20))
    app_key = Column(Unicode(50))
    user_name = Column(Unicode(50))
    access_token = Column(Unicode(200))
    token_created_at = Column(DateTime)
    expired_at = Column(DateTime)
    token = Column(Unicode(200))
    updated_at = Column(DateTime)
    updated_user = Column(Unicode(20))

set_of_books = SetOfBook.__table__


class Device(Base):
    __tablename__ = 'devices'

    id = Column(Integer, primary_key=True)
    set_of_book = Column(Unicode(20))
    name = Column(Unicode(50))
    dev_id = Column(Integer)
    store_id = Column(Integer)
    bank_id = Column(Integer)
    member_id = Column(Integer)
    employee_id = Column(Integer)
    bill_type = Column(Integer)
    created_at = Column(DateTime)
    created_user = Column(Unicode(20))
    updated_at = Column(DateTime)
    updated_user = Column(Unicode(20))

devices = Device.__table__



class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True)
    set_of_book = Column(Unicode(20))
    trans_id = Column(Unicode(100))
    status = Column(Integer)
    e_id = Column(Unicode(50))
    dev_id = Column(Integer)
    create_time = Column(DateTime)
    update_time = Column(DateTime)
    total_amount = Column(Float)
    products = Column(MutableDict.as_mutable(JSON))
    created_at = Column(DateTime)
    created_user = Column(Unicode(20))
    updated_at = Column(DateTime)
    updated_user = Column(Unicode(20))
    is_imported = Column(Boolean, default=False)
    imported_at = Column(DateTime)
    imported_user = Column(Unicode(50))
    retail_id = Column(Integer)
    retail_code = Column(Unicode(50))
    
orders = Order.__table__

