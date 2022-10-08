
from schemas.mongo_models.device_models import MongoDevice, GeoJson2DPoint, MongoDeviceDataEntry
from schemas.mongo_models.account_models import MongoCompanyAccount, MongoCompany
from passlib.context import CryptContext
from beanie import init_beanie
import motor
import asyncio
import time
import math
import os
import sys
import random
cwd = os.getcwd()
sys.path.append(cwd)


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def main():
    client = motor.motor_asyncio.AsyncIOMotorClient(
        os.environ['mongo_database_url'])
    await init_beanie(database=client['test'] if os.environ['ENV'] == 'DEV' else client['main'], document_models=[MongoCompany, MongoCompanyAccount, MongoDevice])
    print('making')
    # mongo_company = MongoCompany.construct()
    # mongo_company.name = 'test'
    # await mongo_company.save()

    # mongo_account = MongoCompanyAccount.construct()
    # mongo_account.email = 'test'
    # mongo_account.password_hash = pwd_context.hash('test')
    # mongo_account.company_id = mongo_company.id
    # await mongo_account.save()

    company = await MongoCompany.find_one(MongoCompany.name == 'test')
    # company.labels = {
    # }
    # await company.save()

    device: MongoDevice = MongoDevice.construct()
    device.device_id = 10
    device.device_secret = 20
    device.aes_key = b'\x12!\xfbLT\xf6\xd1YY}\xc9\xd4i\xdb\xb9\x92'
    device.data = []
    device.past_day_data = []
    device.past_week_data = []
    device.past_month_data = []
    device.past_year_data = []
    date = int(time.time()) - 24*60*60
    # for i in range(24*2):
    #     entry = MongoDeviceDataEntry.construct()
    #     entry.time_s = date + i*30*60
    #     entry.distance_mm = 50 * math.sin(i*math.pi*2/24-2)
    #     device.past_day_data.append(entry)
    device.company_id = company.id
    device.creation_date = int(time.time())
    device.location = GeoJson2DPoint(coordinates=(51.500 + (random.randint(-500, 500) / 10000),
                                                  -0.1743 + (random.randint(-500, 500) / 10000)))
    device.warning_level = 5
    device.warning_level_percentage = 50
    device.installation_comment = ''
    device.comments = ''
    device.pinned = False
    await device.save()
    print(device)

    for i in range(20):
        i = i * 10 + 50
        device: MongoDevice = MongoDevice.construct()
        device.device_id = i
        device.device_secret = 30
        device.aes_key = b'\x12!\xfbLT\xf6\xd1YY}\xc9\xd4i\xdb\xb9\x92'
        device.data = []
        device.past_day_data = []
        device.past_week_data = []
        device.past_month_data = []
        device.past_year_data = []
        date = int(time.time()) - 24*60*60
        for i in range(24*2):
            entry = MongoDeviceDataEntry.construct()
            entry.time_s = date + i*30*60
            entry.distance_mm = 50 * math.sin(i*math.pi*2/24)
            device.past_day_data.append(entry)
        device.company_id = company.id
        device.creation_date = int(time.time())
        device.location = GeoJson2DPoint(
            coordinates=(51.498 + (random.randint(-3000, 3000) / 10000),
                         -0.1832 + (random.randint(-3000, 3000) / 10000))
        )
        device.warning_level = 5
        device.setup_complete = True
        device.warning_level_percentage = 50
        device.installation_comment = ''
        device.comments = ''
        device.pinned = False
        await device.save()
        print('made')


asyncio.run(main())
