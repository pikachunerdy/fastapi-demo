from beanie import Document
from beanie.odm.fields import PydanticObjectId
from pydantic import BaseModel

class MongoCompany(Document):
    class DocumentMeta:
      collection_name = "mongo-companies"
    # company_id : int
    name : str
    labels : dict[str,list[PydanticObjectId]] = {}

class MongoPermissions(BaseModel):
    view_devices : bool = False
    register_devices : bool = False
    manage_devices : bool = False
    manage_accounts : bool = False
    view_device_data : bool = False
    account_id : bool = False

class MongoCompanyAccount(Document):
    class DocumentMeta:
      collection_name = "mongo-company-accounts"
    email : str
    password_hash : str
    permissions : MongoPermissions = MongoPermissions()
    company_id : int
    master_account : bool = False
