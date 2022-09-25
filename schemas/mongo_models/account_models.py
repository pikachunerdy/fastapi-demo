'''Models representing company accounts and company information'''

from typing import NewType
from beanie import Document
from beanie.odm.fields import PydanticObjectId
from pydantic import BaseModel

LabelName = NewType('LabelName',str)

class MongoCompany(Document):
    '''Mongo Company'''
    class DocumentMeta:
        '''Meta Data'''
        collection_name = "mongo-companies"

    name : LabelName
    labels : dict[LabelName,list[PydanticObjectId]] = {}

class MongoPermissions(BaseModel):
    '''Account permissions'''
    view_devices : bool = False
    register_devices : bool = False
    manage_devices : bool = False
    manage_accounts : bool = False
    view_device_data : bool = False
    account_id : bool = False

class MongoCompanyAccount(Document):
    '''Representation of a company account'''
    class DocumentMeta:
        '''Metadata'''
        collection_name = "mongo-company-accounts"
    email : str
    password_hash : str
    permissions : MongoPermissions = MongoPermissions()
    company_id : PydanticObjectId
    master_account : bool = False
