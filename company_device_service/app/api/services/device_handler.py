from app.api.models.models.device_models import Device, DeviceData, DeviceInfo, DeviceSearchFilter, Devices
from schemas.mongo_models.account_models import MongoCompany
from schemas.mongo_models.device_models import GeoJson2DPoint, MongoDevice
from typing import List
from beanie.odm.fields import PydanticObjectId

from app.api.models.models.device_models import DeviceInfo, DeviceSearchFilter, Devices
from app.api.models.models.device_models import DeviceData, Measurement
import datetime
from beanie.odm.operators.find.geospatial import NearSphere
from beanie.odm.operators.find.comparison import In

def mongo_device_to_device_data(mongo_device : MongoDevice, mongo_company : MongoCompany, measurement_period_type : str) -> DeviceData:
    def unix_to_date(unix : int, use_time = True, use_date = False) -> str:
        dt = datetime.datetime.fromtimestamp(unix)
        response = ''
        if use_date:
            response += str(dt.date())
        if use_date and use_time:
            response += ' '
        if use_time:
            response += str(dt.time())
        return response

    device : DeviceData = DeviceData.construct()
    device.creation_date = mongo_device.creation_date
    device.warning_level = str(mongo_device.warning_level)
    device.warning_level_percentage = mongo_device.warning_level_percentage

    if measurement_period_type == 'all':
        device.measurements = [Measurement(time_s = unix_to_date(measurement.time_s, use_date=True), distance_mm = measurement.distance_mm) for measurement in mongo_device.data]
    if measurement_period_type == 'day':
        device.measurements = [Measurement(time_s = unix_to_date(measurement.time_s), distance_mm = measurement.distance_mm) for measurement in mongo_device.past_day_data]
    if measurement_period_type == 'week':
        device.measurements = [Measurement(time_s = unix_to_date(measurement.time_s, use_date=True, use_time=True), distance_mm = measurement.distance_mm) for measurement in mongo_device.past_week_data]
    if measurement_period_type == 'month':
        device.measurements = [Measurement(time_s = unix_to_date(measurement.time_s, use_date=True, use_time=False), distance_mm = measurement.distance_mm) for measurement in mongo_device.past_month_data]
    if measurement_period_type == 'year':
        device.measurements = [Measurement(time_s = unix_to_date(measurement.time_s, use_date=True, use_time=False), distance_mm = measurement.distance_mm) for measurement in mongo_device.past_year_data]
        # print(device.measurements)

    device.device_id = str(mongo_device.device_id)
    device.latitude = mongo_device.location.coordinates[0]
    device.longitude = mongo_device.location.coordinates[1]
    device.comments = mongo_device.comments
    device.installation_comment = mongo_device.installation_comment
    device.pinned = mongo_device.pinned
    device.measurement_period_type = measurement_period_type
    device.labels = []
    device.battery_percentage = mongo_device.battery_percentage
    device.current_level_percentage = mongo_device.current_level_percentage
    device.max_distance_mm = mongo_device.max_distance_mm
    for label, labeled_devices in mongo_company.labels.items():
        if mongo_device.id in labeled_devices:
            device.labels.append(label)
    return device

def mongo_device_to_device_info(mongo_device : MongoDevice, mongo_company : MongoCompany) -> DeviceInfo:
    device_info : DeviceInfo = DeviceInfo.construct()
    device_info.latitude = mongo_device.location.coordinates[0]
    device_info.longitude = mongo_device.location.coordinates[1]
    device_info.creation_date = mongo_device.creation_date
    device_info.warning_level = str(mongo_device.warning_level)
    device_info.warning_level_percentage = mongo_device.warning_level_percentage
    device_info.device_id = str(mongo_device.device_id)
    device_info.pinned = mongo_device.pinned
    device_info.installation_comment = mongo_device.installation_comment
    device_info.comments = mongo_device.comments
    device_info.labels = []
    device_info.battery_percentage = mongo_device.battery_percentage
    device_info.current_level_percentage = mongo_device.current_level_percentage
    device_info.max_distance_mm = mongo_device.max_distance_mm
    for label, labeled_devices in mongo_company.labels.items():
        if mongo_device.id in labeled_devices:
            device_info.labels.append(label)
    return device_info

def mongo_devices_to_devices(mongo_devices : List[MongoDevice], mongo_company : MongoCompany, filter : DeviceSearchFilter) -> Devices:
    devices = Devices.construct()
    devices.search_filter = filter
    devices.devices = [mongo_device_to_device_info(mongo_device,mongo_company) for mongo_device in mongo_devices]
    return devices

class DeviceHandler:

    _mongo_device : MongoDevice
    _mongo_company : MongoCompany

    @classmethod
    async def create(klass, company_id : str, device_id : str):
        device = await MongoDevice.find(MongoDevice.device_id == int(device_id)).first_or_none()
        company = await MongoCompany.get(company_id)
        # print(device)
        print(device)
        if str(device.company_id) != str(company_id):
            raise Exception
        if company is None:
            raise Exception
        handler =  klass()
        handler._mongo_device = device
        handler._mongo_company = company
        return handler

    @staticmethod
    async def get_devices(device_filter : DeviceSearchFilter, company_id : str) -> Devices:
        # company_id = int(company_id)
        mongo_devices = MongoDevice.find(MongoDevice.company_id == PydanticObjectId(company_id))
        print('hello')
        print(company_id)
        mongo_company = await MongoCompany.get(PydanticObjectId(company_id))
        if mongo_company is None:
            raise Exception
        if device_filter.warning_level is not None:
            mongo_devices = mongo_devices.find(MongoDevice.warning_level == device_filter.warning_level)
        if device_filter.pinned:
            mongo_devices = mongo_devices.find(MongoDevice.pinned == True)
        if device_filter.latitude is not None and device_filter.longitude is not None and device_filter.distance is not None:
            mongo_devices = mongo_devices.find(NearSphere(MongoDevice.location,device_filter.longitude, device_filter.latitude, device_filter.distance))
        mongo_devices = mongo_devices.to_list()
        mongo_devices = await mongo_devices
        if device_filter.labels is not None and len(device_filter.labels) > 0:
            filtered_by_label_mongo_devices = []
            for mongo_device in mongo_devices:
                for label in device_filter.labels:
                    print(label)
                    print( device_filter.labels)
                    if not label in mongo_company.labels:
                        print('label does not exist')
                        continue
                    if mongo_device.id in mongo_company.labels[label]:
                        print('device in label')
                        filtered_by_label_mongo_devices.append(mongo_device)
                        break
            mongo_devices = filtered_by_label_mongo_devices
        if device_filter.start_index is not None and device_filter.end_index is not None:
            mongo_devices = mongo_devices[device_filter.start_index:device_filter.end_index]
        return mongo_devices_to_devices(mongo_devices, mongo_company, device_filter)

    def get_device_data(self, measurement_period_type : str) -> DeviceData:
        return mongo_device_to_device_data(self._mongo_device, self._mongo_company, measurement_period_type)

    async def modify(self, new_device : Device) -> DeviceInfo:
        self._mongo_device.comments = new_device.comments
        self._mongo_device.warning_level_percentage = new_device.warning_level_percentage
        self._mongo_device.pinned = new_device.pinned
        self._mongo_device.location = GeoJson2DPoint(coordinates=(new_device.latitude, new_device.longitude))
        await self._mongo_device.save()
        return mongo_device_to_device_info(self._mongo_device, self._mongo_company)

    async def delete(self):
        await self._mongo_device.delete()
