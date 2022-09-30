from pydantic import BaseModel, Field
from pydantic.types import Optional, List

class DeviceSearchFilter(BaseModel):
    latitude : Optional[float] = Field(None,description="degrees of latitude of centre of search circle")
    longitude : Optional[float] = Field(None,description="degrees of longitude of centre of search circle")
    distance : Optional[float] = Field(None,description="radius of search circle in meters")
    warning_level : Optional[int] = Field(None,description="filter for devices with this warning level")
    start_index : int = Field(None, description="start index for list of devices")
    end_index : int = Field(None, description="end index for list of devices")
    labels : list[str] = []
    pinned : bool = Field(False, description="enables only showing pinned devices")

class Device(BaseModel):
    device_id : str
    latitude : float
    longitude : float
    warning_level_percentage : int
    comments : str = ''
    pinned : bool


class DeviceInfo(Device):
    creation_date : int = Field(description="creation date in unix time seconds")
    warning_level : int
    max_distance_mm : int
    current_level_percentage : int
    battery_percentage: int
    installation_comment : str
    labels : list[str]

class Measurement(BaseModel):
    time_s : str = Field(description="unix time in seconds of a measurement")
    distance_mm : float = Field(description="distance measured by the sensor in mm")

class DeviceData(DeviceInfo):
    measurements : Optional[List[Measurement]]
    measurement_period_type : str = ''

class Devices(BaseModel):
    devices : List[DeviceInfo]
    search_filter : DeviceSearchFilter

class SetupInfo(BaseModel):
    height : int
