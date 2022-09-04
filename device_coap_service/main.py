import requests
import os
import asyncio

import aiocoap.resource as resource
import aiocoap
from schemas.encodings.device_server_encoding import DeviceServerEncoding

from schemas.request_models.device_service.device_measurements import DeviceServerMessage, Measurements
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
    def decode_measurement(payload_bytes : bytes) -> DeviceServerMessage:

        encoder = Encoder(DeviceServerEncoding)
        if not encoder.validate_header(payload_bytes):
            raise Exception
        device_server_message = DeviceServerMessage.construct()
        device_id = encoder.get_id(payload_bytes)
        # TODO request key from device service
        aes_key = b'\x12!\xfbLT\xf6\xd1YY}\xc9\xd4i\xdb\xb9\x92'
        payload_bytes = encoder.decrypt(payload_bytes, aes_key)
        device_server_encoding : DeviceServerEncoding = encoder.decode_bytes(payload_bytes)
        device_server_message.device_id = device_id
        device_server_message.device_secret = device_server_encoding.device_secret
        device_server_message.measurements = Measurements.construct()
        device_server_message.measurements.time_s = []
        device_server_message.measurements.distance_mm = []
        # print(device_server_encoding.measurements)
        for measurement in device_server_encoding.measurements:
            device_server_message.measurements.time_s.append(measurement.time)
            device_server_message.measurements.distance_mm.append(measurement.distance)
        # print(payload)
        return device_server_message

    async def render_post(self, request):
        try:
            # TODO decrypt the bytes first
            device_server_message = MeasurementsHandler.decode_measurement(request.payload)
        except:
            return aiocoap.Message(payload=bytes(''))
        response = requests.post(environmentSettings.measurements_api, data=device_server_message.json())
        # TODO encrypt the message first
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
