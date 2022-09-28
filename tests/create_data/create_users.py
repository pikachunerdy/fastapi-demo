
import asyncio
import motor
from beanie import init_beanie
from passlib.context import CryptContext


import os
cwd = os.getcwd()
import sys
sys.path.append(cwd)

from schemas.mongo_models.account_models import MongoCompanyAccount, MongoCompany


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def main():
    client = motor.motor_asyncio.AsyncIOMotorClient('mongodb://localhost:27017/')
    await init_beanie(database=client.db_name, document_models=[MongoCompany,MongoCompanyAccount])
    print('making')
    mongo_company = MongoCompany.construct()
    mongo_company.name = 'test'
    await mongo_company.save()

    mongo_account = MongoCompanyAccount.construct()
    mongo_account.email = 'test'
    mongo_account.password_hash = pwd_context.hash('test')
    mongo_account.company_id = mongo_company.id
    await mongo_account.save()
    print('made')

asyncio.run(main())
