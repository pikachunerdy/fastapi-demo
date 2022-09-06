from beanie import Document
from beanie.odm.fields import PydanticObjectId
from pydantic import BaseModel

class MongoService(Document):
    class DocumentMeta:
        collection_name = "mongo-service"
    name : str
    api_keys = []
