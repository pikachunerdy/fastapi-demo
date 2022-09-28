
import asyncio
import motor
from beanie import init_beanie
from passlib.context import CryptContext


import os
cwd = os.getcwd()
import sys
sys.path.append(cwd)

from schemas.mongo_models.account_models import MongoCompanyAccount, MongoCompany, MongoPermissions


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def main():
    client = motor.motor_asyncio.AsyncIOMotorClient(os.environ['mongo_database_url'] )
    await init_beanie(database=client['test'] if os.environ['ENV'] == 'DEV' else client['main'], document_models=[MongoCompany,MongoCompanyAccount])
    print('making')
    mongo_company = MongoCompany.construct()
    mongo_company.name = 'test'
    await mongo_company.save()

    mongo_account = MongoCompanyAccount.construct()
    mongo_account.email = 'test'
    mongo_account.password_hash = pwd_context.hash('test')
    mongo_account.company_id = mongo_company.id
    permissions = MongoPermissions.construct()
    permissions.manage_accounts = True
    permissions.manage_devices = True
    permissions.view_device_data = True
    permissions.view_devices = True
    permissions.register_devices = True
    mongo_account.permissions = permissions
    await mongo_account.save()
    print('made')

asyncio.run(main())
