import math
import paho.mqtt.client as mqtt
from random import randrange, uniform
import time
from Crypto.Cipher import AES
from os import urandom

mqttBroker ="127.0.0.1"

client = mqtt.Client()
client.connect(mqttBroker, port=2883)


start_time = int(time.time())
measurements = []
for i in range(start_time-60*60*24*7*10,start_time,4*60*60):
# for i in range(start_time,start_time+60*60*24,4*60*60):
    measurement = int((math.sin((i-start_time)/(60*60*24*7)*math.pi*2)+2)*100)
    times = i.to_bytes(4,'little', signed = False)
    # print('time', i)
    # print([int(x)&255 for x in times])
    measurement = measurement.to_bytes(2,'little', signed = False)
    measurements = measurements + [int(x)&255 for x in times]
    measurements = measurements + [int(x)&255  for x in measurement]

# measurements = [10,0,0,0,3,0,15,0,0,0,7,0]
num_measurements = [int(x) for x in int(len(measurements)/6).to_bytes(2,'little', signed = False)]
# print('num',num_measurements)
device_id = [10,0,0,0]
device_secret = [20,0,0,0]
# print(max([0,hash_sum] + device_id + num_measurements + measurements))

iv=urandom(16)
cipher = AES.new(b'\x12!\xfbLT\xf6\xd1YY}\xc9\xd4i\xdb\xb9\x92', AES.MODE_CFB, IV=iv)
byte_array = bytearray(device_secret + num_measurements  + measurements)
message = cipher.encrypt(byte_array)
iv = [int(x) for x in iv]
message = [int(x) for x in message]

hash_sum = (sum(iv+message+device_id)) & 255
payload = bytearray([0,hash_sum] + device_id + iv + message)
# payload = bytearray([0,hash_sum] + device_id + num_measurements + measurements)
print([int(x) for x in payload])
client.publish("MEASUREMENTS", payload)
print('published')
time.sleep(1)


# HEADER
# SUM
# DEVICE ID

# IV
# DEVICE SECRET
# MEASUREMENTS
