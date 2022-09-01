from pydantic import  BaseModel

class Settings(BaseModel):
    sleep_time_s : int
    transmit_time_s : int
