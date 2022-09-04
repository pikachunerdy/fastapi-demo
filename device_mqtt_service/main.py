import requests
import paho.mqtt.client as mqtt
import time
from configs.configs import environmentSettings
print(environmentSettings)
from schemas.encodings.device_server_encoding import DeviceServerEncoding
from schemas.request_models.device_service.device_measurements import DeviceServerMessage, Measurements
from libs.byte_encoder.encoder import Encoder

time.sleep(5)

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

def on_message(client, userdata, message):
    print([int(x) for x in message.payload])
    device_server_message = decode_measurement(message.payload)
    # print("received message: " ,str(message.payload.decode("utf-8")))
    response = requests.post(environmentSettings.measurements_api, data=device_server_message.json())
    print(response)
    print(client)


mqttBroker ="127.0.0.1"

client = mqtt.Client()
client.connect(mqttBroker, port = 2883)

client.subscribe("MEASUREMENTS")
client.on_message=on_message
client.loop_forever()
