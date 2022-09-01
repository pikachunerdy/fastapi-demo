from pydantic import BaseModel


class Measurements(BaseModel):
    time_s : list[int]
    distance_mm : list[int]

class Payload(BaseModel):
    measurements : Measurements
    device_id : int
