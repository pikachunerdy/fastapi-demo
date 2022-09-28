import requests
import os
import asyncio

import aiocoap.resource as resource
import aiocoap
from schemas.encodings.device_server_encoding import DeviceServerEncoding, ServerDeviceEncoding

from schemas.request_models.device_service.device_settings import Settings
from schemas.request_models.device_service.device_measurements import DeviceServerMessage, Measurements
from schemas.request_models.device_service.device_settings import Settings
from libs.byte_encoder.encoder import TemplateBase, Encoder
from configs.configs import environmentSettings, Config

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
    def decode_measurement(payload_bytes: bytes) -> tuple[DeviceServerMessage, bytes]:
        '''Convert coap bytes to DeviceServer Message'''
        encoder = Encoder(DeviceServerEncoding)
        if not encoder.validate_header(payload_bytes):
            raise Exception
        device_server_message = DeviceServerMessage.construct()
        device_id = encoder.get_id(payload_bytes)
        aes_key = requests.get(
            (environmentSettings.DEVICE_SERVICE_URL +
             Config.aes_api + '?device_id=' + str(device_id)),
            headers={environmentSettings.API_KEY_NAME: environmentSettings.API_KEY, })
        aes_key = aes_key.content
        # payload_bytes = encoder.decrypt(payload_bytes, aes_key)
        device_server_encoding: DeviceServerEncoding = encoder.decode_bytes(
            payload_bytes, encryption_key=aes_key)
        device_server_message.device_id = device_id
        device_server_message.device_secret = device_server_encoding.device_secret
        device_server_message.measurements = Measurements.construct()
        device_server_message.measurements.time_s = []
        device_server_message.measurements.distance_mm = []
        for measurement in device_server_encoding.measurements:
            device_server_message.measurements.time_s.append(measurement.time)
            device_server_message.measurements.distance_mm.append(
                measurement.distance)
        return device_server_message, aes_key

    async def render_post(self, request):
        '''Response to a post request'''
        # try:
        print('received message')
        device_server_message, aes_key = MeasurementsHandler.decode_measurement(
            request.payload)
        response = requests.post(
            (environmentSettings.DEVICE_SERVICE_URL + Config.measurements_api),
            data=device_server_message.json(),
            headers={environmentSettings.API_KEY_NAME: environmentSettings.API_KEY})
        settings = Settings(**response.json())
        encoded_settings = ServerDeviceEncoding()
        encoded_settings.measurement_sleep_time_s = settings.measurement_sleep_time_s
        encoded_settings.message_wait_time_s = settings.message_wait_time_s
        encoded_settings.warning_distance_mm = 0
        encoded_settings.warning_measurement_sleep_time_s = 0
        encoded_settings.warning_message_wait_time_s = 0
        encoded_settings.code_version = 1
        # print(response.content)
        # print(response.json())
        encoder = Encoder(ServerDeviceEncoding)
        payload = encoder.encode_bytes(encoded_settings, encryption_key=aes_key)
        decoded_payload = encoder.decode_bytes(payload, encryption_key = aes_key)
        return aiocoap.Message(
            payload=payload)
        # except Exception:
        #     return aiocoap.Message(payload=bytes())


async def main():
    '''App entry point'''
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
