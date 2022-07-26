from schemas.device_mongo_models.device_models import GeoJson2DPoint, MongoDevice
from app.api.main import app
import time
@app.get('/create_device', tags = ["Tests"])
async def create_device():
    device = MongoDevice.construct()
    device.data = []
    device.past_day_data = [] 
    device.past_week_data = []
    device.past_month_data = []
    device.past_year_data = []
    device.company_id = 0
    device.creation_date = int(time.time())
    device.location = GeoJson2DPoint(coordinates=(51.500,-0.1743))
    device.warning_level = 5
    device.warning_level_height_mm  = 50
    device.installation_comment = ''
    device.comments = []
    device.pinned = False
    await device.save()
    print('saved')
    
    device = MongoDevice.construct()
    device.data = []
    device.past_day_data = [] 
    device.past_week_data = []
    device.past_month_data = []
    device.past_year_data = []
    device.company_id = 0
    device.creation_date = int(time.time())
    device.location = GeoJson2DPoint(coordinates=(51.498,-0.1832))
    device.warning_level = 5
    device.warning_level_height_mm  = 50
    device.installation_comment = ''
    device.comments = []
    device.pinned = False
    await device.save()
    print('saved')