import requests
import os
import asyncio

import aiocoap.resource as resource
import aiocoap

from schemas.request_models.device_service.device_measurements import Payload, Measurements
from schemas.request_models.device_service.device_settings import Settings
from libs.byte_encoder.encoder import TemplateBase, Encoder
from configs.configs import environmentSettings

URL = environmentSettings.measurements_api
#  'http://localhost:8002/measurements' if environmentSettings.ENV == 'DEV' else 'url'


class Update(resource.Resource):

    async def render_get(self, request):
        print(request)
        # TODO design
        # message = json.loads(request.payload)
        return aiocoap.Message(payload='')


class MeasurementEncoding(TemplateBase):
    time = (int, 4)
    distance = (int, 2)


class DeviceServerEncoding(TemplateBase):
    '''
    The received messages should be of the form
    0-1: 1 byte: Start of message = 0
    1-2: 1 byte: sum of all the bytes
    2-6: 4 byte: Device ID
    6-8: 2 byte: Num reading
    8-8+6*num_readings
    For each reading
        4 bytes time, 2 bytes distance
    '''
    device_id = (int,4)
    measurements = (list,MeasurementEncoding)

class ServerDeviceEncoding(TemplateBase):
    message_wait_time = (int,2)
    measurement_sleep_time = (int,2)
    warning_distance = (int,2)
    warning_message_wait_time = (int,2)
    warning_measurement_sleep_time = (int,2)


class MeasurementsHandler(resource.Resource):

    '''
    The received messages should be of the form
    0-1: 1 byte: Start of message = 0
    1-2: 1 byte: sum of all the bytes
    2-6: 4 byte: Device ID
    6-8: 2 byte: Num reading
    8-8+6*num_readings
    For each reading
        4 bytes time, 2 bytes distance

    The returned message should be of the form
    0-1: 1 byte: Start of message = 0
    1-2: 1 byte: sum of all the bytes
    2-4: 2 byte: message_wait_time
    4-6: 2 byte: measurement_sleep_time
    6-8: 2 byte: warning distance
    8-10: 2 byte: warning message_wait_time
    10-12: 2 byte: warning measurement_sleep_time
    '''

    @staticmethod
    def decode_measurement(payload_bytes : bytes) -> Payload:
        # payload = Payload.construct()
        # payload.measurements = Measurements.construct()
        # payload.measurements.time_s = []
        # payload.measurements.distance_mm = []

        # if payload_bytes[0] != 0:
        #     raise Exception

        # payload_hash = int(payload_bytes[1])
        # current_hash = 0
        # for byte in payload_bytes[2:]:
        #     current_hash += byte
        # current_hash = int(current_hash & 255)

        # if current_hash != payload_hash:
        #     print('bad hash', current_hash, payload_hash)
        #     raise Exception

        # payload.device_id = int.from_bytes(payload_bytes[2:6],'little', signed=False)
        # print(payload.device_id)
        # num_measurements = int.from_bytes(payload_bytes[6:8],'little', signed=False)
        # print(num_measurements)

        # for i in range(num_measurements):
        #     time_bytes = payload_bytes[8+i*6: 8+i*6+4]
        #     distance_bytes = payload_bytes[8+i*6+4: 8+i*6+6]
        #     print(time_bytes)
        #     print(distance_bytes)
        #     payload.measurements.time_s.append(int.from_bytes(time_bytes,'little', signed=False))
        #     payload.measurements.distance_mm.append(int.from_bytes(distance_bytes,'little', signed=False))

        payload = Payload.construct()
        encoder = Encoder(DeviceServerEncoding)
        device_server_encoding : DeviceServerEncoding = encoder.decode_bytes(payload_bytes)
        payload.device_id = device_server_encoding.device_id
        payload.measurements = Measurements.construct()
        payload.measurements.time_s = []
        payload.measurements.distance_mm = []
        # print(device_server_encoding.measurements)
        for measurement in device_server_encoding.measurements:
            payload.measurements.time_s.append(measurement.time)
            payload.measurements.distance_mm.append(measurement.distance)
        # print(payload)
        return payload

    async def render_post(self, request):
        print('POST Message')
        try:
            payload = MeasurementsHandler.decode_measurement(request.payload)
        except:
            return aiocoap.Message(payload=bytes(''))
        print('Testing')
        response = requests.post(environmentSettings.measurements_api, data=payload.json())
        print('Received Message')
        return aiocoap.Message(payload=bytes('hello','utf8'))

async def main():
    # Resource tree creation
    root = resource.Site()
    root.add_resource(['.well-known', 'core'],
            resource.WKCResource(root.get_resources_as_linkheader))
    root.add_resource(['update'], Update())
    root.add_resource(['measurements'], MeasurementsHandler())
    print('COAP Running')
    await aiocoap.Context.create_server_context(root)

    # Run forever
    await asyncio.get_running_loop().create_future()

if __name__ == "__main__":
    asyncio.run(main())
