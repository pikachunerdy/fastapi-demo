from beanie import Document


class MongoAdminAccount(Document):
    class DocumentMeta:
      collection_name = "mongo-company-accounts"
    email : str
    password_hash : str
