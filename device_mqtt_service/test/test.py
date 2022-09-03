import math
import paho.mqtt.client as mqtt
from random import randrange, uniform
import time

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
hash_sum = (sum(num_measurements) + sum(measurements)+sum(device_id)) & 255
# print(max([0,hash_sum] + device_id + num_measurements + measurements))
payload = bytearray([0,hash_sum] + device_id + num_measurements + measurements)

client.publish("MEASUREMENTS", payload)
print('published')
time.sleep(1)
