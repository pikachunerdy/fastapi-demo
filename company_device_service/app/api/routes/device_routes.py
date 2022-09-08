from typing import Optional
from fastapi.param_functions import Body, Depends
from libs.authentication.user_token_auth import  TokenData, token_authentication
from app.api.main import app
from app.api.models.models.device_models import Device, DeviceData, DeviceInfo, DeviceSearchFilter, Devices
from app.api.routes.tools.validate_token import validate_token
from app.api.services.device_handler import DeviceHandler
from fastapi import Query


@app.get('/devices', response_model=Devices, tags=["Device Info"])
async def get_devices(
    latitude : Optional[float] = None,
    longitude : Optional[float] = None,
    distance : Optional[float] = None,
    warning_level : Optional[int] = None,
    start_index : int = None,
    end_index : int = None,
    labels : list[str] =  Query(default=[]),
    pinned : bool = None,
    token_data : TokenData = Depends(token_authentication)) -> Devices:
    '''Request a list of Devices,
    can use filters such as nearest to a coordinate or at a certain warning level,
    requires view_devices permission'''
    if labels is None:
        labels = []
    if '' in labels: labels.remove('')
    print(labels)
    device_filter : DeviceSearchFilter = DeviceSearchFilter(
        latitude = latitude,
        longitude = longitude,
        distance = distance,
        warning_level = warning_level,
        start_index = start_index,
        end_index = end_index,
        labels  = labels,
        pinned = pinned,
    )
    validate_token(token_data.permission.view_devices, token_data)
    devices = await DeviceHandler.get_devices(device_filter, token_data.company_id)
    return devices

@app.get('/device', response_model=DeviceData, tags=["Device Info"])
async def get_device(device_id : str, measurement_period_type : str,
    token_data : TokenData = Depends(token_authentication)) -> DeviceData:
    '''Request a specific Device, requires view_device_data permission'''
    validate_token(token_data.permission.view_device_data, token_data)
    handler = await DeviceHandler.create(token_data.company_id, device_id)
    return handler.get_device_data(measurement_period_type)

@app.put('/device', response_model=DeviceInfo, tags=["Device Info"])
async def put_device(device : Device = Body(...),
    token_data : TokenData = Depends(token_authentication)) -> DeviceInfo:
    '''Allows modification of a device, requires manage_device permission'''
    validate_token(token_data.permission.manage_devices, token_data)
    handler = await DeviceHandler.create(token_data.company_id, device.device_id)
    return await handler.modify(device)

@app.delete('/device', tags=["Device Info"])
async def delete_device(device_id : str, token_data : TokenData = Depends(token_authentication)):
    '''Requires manage_device permission'''
    validate_token(token_data.permission.manage_devices, token_data)
    return DeviceHandler(token_data.company_id, device_id).delete()
