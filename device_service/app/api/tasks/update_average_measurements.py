import time
from app.api.main import celery
from schemas.mongo_models.device_models import MongoDevice, MongoDeviceDataEntry
from asgiref.sync import async_to_sync

async def process_average_measurements(device_id : str):
    total_measurements_per_period = 24*15
    def average_list(data : list[MongoDeviceDataEntry]):
        measurements = []
        chunks = [data[x:x+total_measurements_per_period]
            for x in range(0, len(data), total_measurements_per_period)]
        for chunk in chunks:
            total_time = 0
            total_distance = 0
            for measurement in chunk:
                total_time += measurement.time_s
                total_distance += measurement.distance_mm
            total_time /= len(chunk)
            total_distance /= len(chunk)
            measurements.append(MongoDeviceDataEntry(time_s = total_time, distance_mm = total_distance))
        return measurements

    # TODO do this in a much better way
    mongo_device = await MongoDevice.find(MongoDevice.device_id == device_id).first_or_none()
    data = mongo_device.data
    print(data)
    last_day = []
    last_week = []
    last_month = []
    last_year = []
    for measurement in data:
        print('hello')
        print(measurement)
        if measurement.time_s - int(time.time()) < (24*60*60):
            last_day.append(measurement)
        if measurement.time_s - int(time.time()) < (7*24*60*60):
            last_week.append(measurement)
        if measurement.time_s - int(time.time()) < (31*24*60*60):
            last_month.append(measurement)
        if measurement.time_s - int(time.time()) < (365*24*60*60):
            last_year.append(measurement)
    mongo_device.past_day_data = average_list(last_day)
    mongo_device.past_week_data = average_list(last_week)
    mongo_device.past_month_data = average_list(last_month)
    mongo_device.past_year_data = average_list(last_year)
    await mongo_device.save()

@celery.task(name="process_average_measurements_task")
async def process_average_measurements_task(device_id : str):
    await process_average_measurements(device_id)
