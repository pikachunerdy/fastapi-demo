'''App entry point'''

import time
import requests

import paho.mqtt.client as mqtt

from libs.byte_encoder.encoder import Encoder
from schemas.request_models.device_service.device_measurements import DeviceServerMessage, Measurements
from schemas.encodings.device_server_encoding import DeviceServerEncoding
from configs.configs import environmentSettings, Config

time.sleep(5)


def decode_measurement(payload_bytes: bytes) -> DeviceServerMessage:
    '''Get the device Server message from the payload bytes'''
    encoder = Encoder(DeviceServerEncoding)
    if not encoder.validate_header(payload_bytes):
        raise Exception
    device_server_message = DeviceServerMessage.construct()
    device_id = encoder.get_id(payload_bytes)
    aes_key = requests.get(
        (environmentSettings.DEVICE_SERVICE_URL + Config.aes_api + '?device_id=' + str(device_id)),
        headers={environmentSettings.API_KEY_NAME: environmentSettings.API_KEY,})
    aes_key = aes_key.content
    print(aes_key)
    # aes_key = b'\x12!\xfbLT\xf6\xd1YY}\xc9\xd4i\xdb\xb9\x92'
    payload_bytes = encoder.decrypt(payload_bytes, aes_key)
    device_server_encoding: DeviceServerEncoding = encoder.decode_bytes(
        payload_bytes)
    device_server_message.device_id = device_id
    device_server_message.device_secret = device_server_encoding.device_secret
    device_server_message.measurements = Measurements.construct()
    device_server_message.measurements.time_s = []
    device_server_message.measurements.distance_mm = []
    for measurement in device_server_encoding.measurements:
        device_server_message.measurements.time_s.append(measurement.time)
        device_server_message.measurements.distance_mm.append(
            measurement.distance)
    return device_server_message


def on_message(_message_client, _user_data, message):
    '''Called when a message is received from a device'''
    device_server_message = decode_measurement(message.payload)
    _ = requests.post(
       ( environmentSettings.DEVICE_SERVICE_URL + Config.measurements_api),
        data=device_server_message.json(),
        headers={environmentSettings.API_KEY_NAME: environmentSettings.API_KEY})


client = mqtt.Client()
print(environmentSettings.MQTTBROKER)
client.connect(environmentSettings.MQTTBROKER, port=2883)

client.subscribe("MEASUREMENTS")
client.on_message = on_message
client.loop_forever()
