from typing import List
from pydantic import BaseModel


class Measurements(BaseModel):
    time_s : List[int]
    distance_mm : List[int]

class DeviceServerMessage(BaseModel):
    battery_percentage : int
    measurements : Measurements
    device_id : int
    device_secret : int
