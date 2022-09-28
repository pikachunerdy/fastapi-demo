from pydantic import  BaseModel

class Settings(BaseModel):
    measurement_sleep_time_s : int
    message_wait_time_s : int
    warning_distance_mm : int = 0
    warning_measurement_sleep_time_s : int = 0
    warning_message_wait_time : int = 0
    code_version : int = 1
