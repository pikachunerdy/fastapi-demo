from beanie import Document
from beanie.odm.fields import PydanticObjectId

class MongoCompany(Document):
    class DocumentMeta:
      collection_name = "mongo-companies"

    company_id : int
    labels : list[str] = []
