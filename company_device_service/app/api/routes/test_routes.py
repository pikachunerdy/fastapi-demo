from asyncio import sleep
from schemas.mongo_models.account_models import MongoCompany
from schemas.mongo_models.device_models import GeoJson2DPoint, MongoDevice, MongoDeviceDataEntry
from app.api.main import app
import math
import time
@app.get('/create_device', tags = ["Tests"])
async def create_device():
    await sleep(5)
    # company = MongoCompany.construct()
    company = await MongoCompany.find_one(MongoCompany.name == 'test')
    # company.company_id = 0
    company.labels = {
    }
    await company.save()

    device : MongoDevice = MongoDevice.construct()
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
    device.location = GeoJson2DPoint(coordinates=(51.500,-0.1743))
    device.warning_level = 5
    device.warning_level_height_mm  = 50
    device.installation_comment = ''
    device.comments = ''
    device.pinned = False
    await device.save()
    print('saved')

    device = MongoDevice.construct()
    device.device_id = 20
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
    device.location = GeoJson2DPoint(coordinates=(51.498,-0.1832))
    device.warning_level = 5
    device.warning_level_height_mm  = 50
    device.installation_comment = ''
    device.comments = ''
    device.pinned = False
    await device.save()
    print('saved')
