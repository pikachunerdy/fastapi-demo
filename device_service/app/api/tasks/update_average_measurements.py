'''Task to update the measurement average information'''

import time
from app.api.main import celery
from schemas.mongo_models.device_models import MongoDevice, MongoDeviceDataEntry


async def process_average_measurements(device_id: int):
    '''Find the daily, weekly, monthly and yearly sensor data'''
    total_measurements_per_period = 24*4

    def average_list(data: list[MongoDeviceDataEntry]):

        measurements = []
        chunk_size = int(len(data) / total_measurements_per_period)
        print('len', len(data))
        print('chunk size', chunk_size)
        chunk_size = chunk_size if chunk_size > 0 else 1
        chunks = [data[x:x+chunk_size]
                  for x in range(0, len(data), chunk_size)]
        for chunk in chunks:
            total_time = 0
            total_distance = 0
            for measurement in chunk:
                total_time += measurement.time_s
                total_distance += measurement.distance_mm
            total_time /= len(chunk)
            total_distance /= len(chunk)
            measurements.append(
                MongoDeviceDataEntry(
                    time_s=total_time, distance_mm=total_distance)
            )
        return measurements

    mongo_device = await MongoDevice.find(MongoDevice.device_id == device_id).first_or_none()
    data = mongo_device.data
    last_day = []
    last_week = []
    last_month = []
    last_year = []
    for measurement in data:
        if int(time.time()) - measurement.time_s < (24*60*60):
            last_day.append(measurement)
        if int(time.time()) - measurement.time_s < (7*24*60*60):
            last_week.append(measurement)
        if int(time.time()) - measurement.time_s < (31*24*60*60):
            last_month.append(measurement)
        if int(time.time()) - measurement.time_s < (365*24*60*60):
            last_year.append(measurement)

    mongo_device.past_day_data = average_list(last_day)
    mongo_device.past_week_data = average_list(last_week)
    mongo_device.past_month_data = average_list(last_month)
    mongo_device.past_year_data = average_list(last_year)

    await mongo_device.save()


@celery.task(name="process_average_measurements_task")
async def process_average_measurements_task(device_id: int):
    '''Task to process the average measurements for a device'''
    await process_average_measurements(device_id)
