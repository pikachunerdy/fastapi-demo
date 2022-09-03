from typing import List
from pydantic import BaseModel


class Measurements(BaseModel):
    time_s : List[int]
    distance_mm : List[int]

class Payload(BaseModel):
    measurements : Measurements
    device_id : int