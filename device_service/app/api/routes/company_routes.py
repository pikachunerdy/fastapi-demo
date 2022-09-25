'''Routes that are accessed from the company account service'''
from fastapi.param_functions import Body, Depends
from fastapi import Response
from app.api.main import app
from app.api.tasks.update_average_measurements import process_average_measurements_task
from app.api.tasks.send_device_settings_mqtt import send_device_settings_mqtt_task

from libs.authentication.inter_service_auth import validate_api_key
from schemas.request_models.device_service.device_measurements import DeviceServerMessage
from schemas.request_models.device_service.device_settings import Settings
from schemas.mongo_models.device_models import MongoDevice, MongoDeviceDataEntry

@app.post('/company_routes/update_device_settings')
async def post_device_settings(device_id: int):
    '''Requests that a message should be sent to the sensor with new device settings'''
    await send_device_settings_mqtt_task(device_id)
