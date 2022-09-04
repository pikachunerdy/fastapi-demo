from pydantic import BaseModel
import json

from app.api.main import app
from schemas.mongo_models.device_models import MongoDevice, MongoDeviceDataEntry
from fastapi import Body
from app.api.tasks.update_average_measurements import process_average_measurements_task
from schemas.request_models.device_service.device_measurements import DeviceServerMessage
from schemas.request_models.device_service.device_settings import Settings
from app.api.configs.configs import environmentSettings


@app.get('/aes_key', response_model=bytes, tags=['key'])
async def get_aes_key(device_id : int, secret : int) -> bytes:
    if secret != environmentSettings.micro_service_key:
        raise Exception()
    mongo_device = await MongoDevice.find(MongoDevice.device_id == device_id).first_or_none()
    if mongo_device is None:
        raise Exception()
    return mongo_device.aes_key

@app.post('/measurements', response_model=Settings, tags=["Measurements"])
async def post_measurements(message : DeviceServerMessage = Body(...)) -> Settings:
    '''Receive device measurements, must be authenticated with device secret'''
    mongo_device = await MongoDevice.find(MongoDevice.device_id == message.device_id).first_or_none()
    if mongo_device is None:
        raise Exception
    # AUTHENTICATE SECRET
    if mongo_device.device_secret != message.device_secret:
        raise Exception

    measurements = message.measurements
    for time_s, distance_mm in zip(measurements.time_s, measurements.distance_mm):
        entry = MongoDeviceDataEntry(time_s=time_s, distance_mm=distance_mm)
        mongo_device.data.append(entry)

    await mongo_device.save()
    # mongo_device = await MongoDevice.find(MongoDevice.device_id == message.device_id).first_or_none()

    response = Settings.construct()
    response.sleep_time_s = mongo_device.sleep_time_s
    response.transmit_time_s = mongo_device.transmit_time_s
    # sends a task request to process average task updates
    await process_average_measurements_task(message.device_id)
    return response
