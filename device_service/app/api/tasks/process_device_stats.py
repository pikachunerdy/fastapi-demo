'''Task to update the measurement average information'''

import time
from app.api.main import celery
from schemas.mongo_models.device_models import MongoDevice, MongoDeviceDataEntry


async def process_device_stats(device_id: int):
    '''Find the daily, weekly, monthly and yearly sensor data'''
    mongo_device: MongoDevice = await MongoDevice.find(MongoDevice.device_id == device_id).first_or_none()
    last_measurement = mongo_device.data[-1].distance_mm
    distance_percentage = last_measurement / mongo_device.max_distance_mm
    mongo_device.warning_level = 10 if distance_percentage < mongo_device.warning_level_percentage else 0
    mongo_device.current_level_percentage = distance_percentage
    await mongo_device.save()


@celery.task(name="process_device_stats_task")
async def process_device_stats_task(device_id: int):
    '''Task to process the average measurements for a device'''
    await process_device_stats(device_id)
