from sqlalchemy import Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import Boolean, Integer, String, List

# TODO add in device setup requests
#   - should contain location information and date information and completion status and device id if completed

Base = declarative_base()
metadata = Base.metadata

class SQLCompany(Base):
    __tablename__ = 'sqlcompanies'
    company_id : int = Column(Integer, primary_key=True, autoincrement=True)
    accounts : list['SQLAccount'] = relationship("SQLAccount", backref="company")
    master_account_id : int = Column(Integer, ForeignKey('sqlaccounts.account_id'))

class SQLAccount(Base):
    __tablename__ = 'sqlaccounts'
    account_id : int = Column(Integer, primary_key=True, autoincrement=True)
    permissions : 'SQLPermissions' = relationship("SQLPermissions", uselist=False, backref="account", cascade = "all, delete, delete-orphan" )
    company_id : int = Column(Integer, ForeignKey('sqlcompanies.company_id'))
    email : str = Column(String(100))
    password_hash : str = Column(String(100))

class SQLPermissions(Base):
    __tablename__ = 'sqlpermissions'
    permissions_id = Column(Integer, primary_key=True, autoincrement=True)
    view_devices = Column(Boolean)
    register_devices = Column(Boolean)
    manage_devices = Column(Boolean)
    manage_accounts = Column(Boolean)
    view_device_data = Column(Boolean)
    account_id = Column(Integer, ForeignKey('sqlaccounts.account_id', use_alter=True))

class SQLService(Base):
    '''Table representing a backend service for inter service authentication'''
    __tablename__ = 'sqlservices'
    service_id : int = Column(Integer, autoincrement=True)
    service_name : str = Column(String(50))
    keys : list['SQLServiceAuthKey'] = relationship("SQLServiceAuthKey", back_populates="service")

class SQLServiceAuthKey(Base):
    '''Authkey that can be used to access a service api'''
    __tablename__ = 'sqlserviceauthkeys'
    key_id : int = Column(Integer, primary_key=True, autoincrement=True)
    key : str = Column(String(64))
    name : str = Column(String(64))
    service : SQLService = relationship("SQLService", back_populates="keys")
