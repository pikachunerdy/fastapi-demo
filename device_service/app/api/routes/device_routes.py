'''Routes for communicating device information'''
from fastapi.param_functions import Body, Depends
from fastapi import Response
from app.api.main import app
from app.api.tasks.update_average_measurements import process_average_measurements_task

from libs.authentication.inter_service_auth import validate_api_key
from schemas.request_models.device_service.device_measurements import DeviceServerMessage
from schemas.request_models.device_service.device_settings import Settings
from schemas.mongo_models.device_models import MongoDevice, MongoDeviceDataEntry


@app.get('/aes_key', response_model=bytes, tags=['key'])
async def get_aes_key(device_id: int, _= Depends(validate_api_key)) -> bytes:
    '''Returns the aes key for a given device_id'''
    mongo_device = await MongoDevice.find(MongoDevice.device_id == device_id).first_or_none()
    if mongo_device is None:
        raise Exception()
    print(mongo_device.aes_key)
    return Response(content=mongo_device.aes_key)
    # return mongo_device.aes_key.decode()


@app.post('/measurements', tags=["Measurements"])
async def post_measurements(
        message: DeviceServerMessage = Body(...), _=Depends(validate_api_key)):
    '''Receive device measurements, must be authenticated with device secret'''
    mongo_device = await MongoDevice.find(
        MongoDevice.device_id == message.device_id
    ).first_or_none()
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
    response.measurement_sleep_time_s = mongo_device.device_settings.measurement_sleep_time_s
    response.message_wait_time_s = mongo_device.device_settings.message_wait_time_s
    # sends a task request to process average task updates
    await process_average_measurements_task(message.device_id)
    return response


# @app.get('/settings', tags=['Measurements'])
# async def
