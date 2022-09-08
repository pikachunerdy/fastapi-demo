from pydantic import  BaseModel

class Settings(BaseModel):
    measurement_sleep_time_s : int
    message_wait_time_time_s : int
    warning_distance_mm : int
    warning_measurement_sleep_time_s : int
    warning_message_wait_time : int
    code_version : int
