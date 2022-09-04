from typing import Tuple
from pydantic import BaseModel
from beanie import Document
import pymongo

class GeoJson2DPoint(BaseModel):
    type: str = "Point"
    coordinates: Tuple[float, float]

class MongoDeviceDataEntry(BaseModel):
    time_s : int
    distance_mm : int

class MongoDevice(Document):
    class DocumentMeta:
      collection_name = "mongo-devices"
    # A unique integer ID given to a device, could be intercepted so treated as public
    device_id : int # should be 4 bytes long
    # A unique integer ID given to a device, kept secret and so used for authentication
    device_secret : int # should be 4 bytes long
    # The key this device is using to encrypt messages
    aes_key : bytes
    data : list[MongoDeviceDataEntry]
    past_day_data : list[MongoDeviceDataEntry]
    past_week_data : list[MongoDeviceDataEntry]
    past_month_data : list[MongoDeviceDataEntry]
    past_year_data : list[MongoDeviceDataEntry]
    company_id : int
    creation_date : int
    location : GeoJson2DPoint
    warning_level : int
    warning_level_height_mm : int
    # any comments made at the point of installation
    installation_comment : str = ''
    # comments made on the device
    comments : str
    pinned : bool = False
    decryption_key : str = ''
    sleep_time_s : int = 15*60*60
    transmit_time_s : int = 24*60*60
    labels : list[str] = []

    class Collection:
        name = "places"
        indexes = [
            [("location", pymongo.GEOSPHERE)],  # GEO index
        ]
MongoDevice.update_forward_refs()
