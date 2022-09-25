'''Mongo Admin Models'''

from beanie import Document


class MongoAdminAccount(Document):
    '''Model storing information for an admin account'''
    class DocumentMeta:
        '''Metadata'''
        collection_name = "mongo-company-accounts"
    email : str
    password_hash : str
