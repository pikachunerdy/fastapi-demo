
import asyncio
import time
import math
from os import urandom
import os

from aiocoap import *
from Crypto.Cipher import AES

from schemas.encodings.device_server_encoding import ServerDeviceEncoding
from libs.byte_encoder.encoder import Encoder


async def main():
    """Perform a single PUT request to localhost on the default port, URI
    "/other/block". The request is sent 2 seconds after initialization.

    The payload is bigger than 1kB, and thus sent as several blocks."""

    context = await Context.create_client_context()

    await asyncio.sleep(10)

    # message = ()

    # for i in range(24*7*10):

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
    byte_array = bytearray(device_secret + [90] + num_measurements  + measurements)
    message = cipher.encrypt(byte_array)
    iv = [int(x) for x in iv]
    message = [int(x) for x in message]

    hash_sum = (sum(iv+message+device_id)) & 255
    payload = bytearray([0,hash_sum] + device_id + iv + message)
    # payload = str(payload, 'UTF-8')
    # print(type(payload))
    url = "coap://206.189.18.234/measurements" if os.environ['ENV'] != 'DEV' else "coap://localhost/measurements"
    request = Message(code=POST, payload=payload, uri=url)
    response = await context.request(request).response
    print(response.payload)
    encoder = Encoder(ServerDeviceEncoding)
    aes_key = b'\x12!\xfbLT\xf6\xd1YY}\xc9\xd4i\xdb\xb9\x92'
    device_id = 10
    response = encoder.decode_bytes(response.payload, encryption_key = aes_key)
    # print('Result: %s\n%r'%(response.code, response.payload))

if __name__ == "__main__":
    asyncio.run(main())
