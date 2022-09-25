'''
Device Mongo Models
'''

from typing import Tuple
from pydantic import BaseModel
from beanie.odm.fields import PydanticObjectId
from beanie import Document
import pymongo

class MongoDeviceSettings(BaseModel):
    '''Settings to be sent to the sensor'''
    message_wait_time_s : int = 24*60*60
    measurement_sleep_time_s : int = 15*60
    warning_distance_mm : int = 0
    warning_message_wait_time_s : int = 24*60*60
    warning_measurement_sleep_time_s : int = 15*60
    code_version : int = 0


class GeoJson2DPoint(BaseModel):
    '''Coordinate Representation'''
    type: str = "Point"
    coordinates: Tuple[float, float]

class MongoDeviceDataEntry(BaseModel):
    '''Individual sensor measurement, time in unix time and distance from sensor'''
    time_s : int
    distance_mm : int

class MongoDevice(Document):
    '''Model representing an individual sensor'''
    class DocumentMeta:
        '''Document MetaData'''
        collection_name = "mongo-devices"
    # A unique integer ID given to a device, could be intercepted so treated as public
    device_id : int # 4 bytes
    # A unique integer ID given to a device, kept secret and so used for authentication
    device_secret : int # 4 bytes
    # The key this device is using to encrypt messages
    aes_key : bytes
    data : list[MongoDeviceDataEntry]
    past_day_data : list[MongoDeviceDataEntry]
    past_week_data : list[MongoDeviceDataEntry]
    past_month_data : list[MongoDeviceDataEntry]
    past_year_data : list[MongoDeviceDataEntry]
    company_id : PydanticObjectId
    creation_date : int
    location : GeoJson2DPoint
    warning_level : int
    warning_level_height_mm : int
    # any comments made at the point of installation
    installation_comment : str = ''
    # comments made on the device
    comments : str = ''
    pinned : bool = False
    decryption_key : str = ''


    device_settings : MongoDeviceSettings = MongoDeviceSettings()

    class Collection:
        '''USed for filtering locations in a given radius'''
        name = "places"
        indexes = [
            [("location", pymongo.GEOSPHERE)],  # GEO index
        ]
MongoDevice.update_forward_refs()
