import requests
import os
import asyncio

import aiocoap.resource as resource
import aiocoap

from schemas.request_models.device_service.device_measurements import Payload, Measurements
from schemas.request_models.device_service.device_settings import Settings
from configs.configs import environmentSettings

URL = environmentSettings.measurements_api
#  'http://localhost:8002/measurements' if environmentSettings.ENV == 'DEV' else 'url'


class Update(resource.Resource):

    async def render_get(self, request):
        print(request)
        # TODO design
        # message = json.loads(request.payload)
        return aiocoap.Message(payload='')

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
    '''

    @staticmethod
    def decode_measurement(payload_bytes : bytes) -> Payload:
        payload = Payload.construct()
        payload.measurements = Measurements.construct()
        payload.measurements.time_s = []
        payload.measurements.distance_mm = []

        if payload_bytes[0] != 0:
            raise Exception

        payload_hash = int(payload_bytes[1])
        current_hash = 0
        for byte in payload_bytes[2:]:
            current_hash += byte
        current_hash = int(current_hash & 255)

        if current_hash != payload_hash:
            print('bad hash', current_hash, payload_hash)
            return aiocoap.Message(payload='')

        payload.device_id = int.from_bytes(payload_bytes[2:6],'little', signed=False)
        print(payload.device_id)
        num_measurements = int.from_bytes(payload_bytes[6:8],'little', signed=False)
        print(num_measurements)

        for i in range(num_measurements):
            time_bytes = payload_bytes[8+i*6: 8+i*6+4]
            distance_bytes = payload_bytes[8+i*6+4: 8+i*6+6]
            print(time_bytes)
            print(distance_bytes)
            payload.measurements.time_s.append(int.from_bytes(time_bytes,'little', signed=False))
            payload.measurements.distance_mm.append(int.from_bytes(distance_bytes,'little', signed=False))

        return payload

    async def render_post(self, request):
        # payload = Payload.construct()
        # payload.measurements = Measurements.construct()
        # payload.measurements.time_s = []
        # payload.measurements.distance_mm = []


        # print([int(x) for x in payload_bytes])

        # TODO add logging here to alert corrupt message
        # if payload_bytes[0] != 0:
        #     print('bad payload')
        #     return aiocoap.Message(payload='')

        # payload_hash = int(payload_bytes[1])
        # current_hash = 0
        # for byte in payload_bytes[2:]:
        #     current_hash += byte
        # current_hash = int(current_hash & 511)

        # TODO add logging here to alert corrupt message
        # if current_hash != payload_hash:
        #     print('bad hash', current_hash, payload_hash)
        #     return aiocoap.Message(payload='')


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

        payload = MeasurementsHandler.decode_measurement(request.payload)
        response = requests.post(environmentSettings.measurements_api, data=payload.json())
        print(response)
        print(response.json())
        print(Settings(**response.json()))
        return aiocoap.Message(payload=bytes('hello','utf8'))

        # message = json.loads(request.payload)
        # print(message)
        # response = requests.post(URL, json=message)
        # response = response.text
        # response = bytes(response,'utf8')
        # return aiocoap.Message(payload=response)

async def main():
    # Resource tree creation
    root = resource.Site()
    root.add_resource(['.well-known', 'core'],
            resource.WKCResource(root.get_resources_as_linkheader))
    root.add_resource(['update'], Update())
    root.add_resource(['measurements'], MeasurementsHandler())

    await aiocoap.Context.create_server_context(root)

    # Run forever
    await asyncio.get_running_loop().create_future()

if __name__ == "__main__":
    asyncio.run(main())
