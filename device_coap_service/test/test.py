
import asyncio

from aiocoap import *
import time
import math

async def main():
    """Perform a single PUT request to localhost on the default port, URI
    "/other/block". The request is sent 2 seconds after initialization.

    The payload is bigger than 1kB, and thus sent as several blocks."""

    context = await Context.create_client_context()

    await asyncio.sleep(3)

    # message = ()

    # for i in range(24*7*10):

    start_time = int(time.time())
    measurements = []

    for i in range(start_time,start_time+60*60*24*7*10,4*60*60):
        measurement = int((math.sin((i-start_time)/(60*60*24*7)*math.pi*2)+2)*100)
        times = i.to_bytes(4,'little', signed = False)
        measurement = measurement.to_bytes(2,'little', signed = False)
        measurements = measurements + [int(x)&255 for x in times]
        measurements = measurements + [int(x)&255  for x in measurement]

    # measurements = [10,0,0,0,3,0,15,0,0,0,7,0]
    num_measurements = [int(x) for x in int(len(measurements)/6).to_bytes(2,'little', signed = False)]
    device_id = [10,0,0,0]
    hash_sum = (sum(num_measurements) + sum(measurements)+sum(device_id)) & 511
    print(max([0,hash_sum] + device_id + num_measurements + measurements))
    payload = bytearray([0,hash_sum] + device_id + num_measurements + measurements)
    # payload = str(payload, 'UTF-8')
    print(type(payload))
    request = Message(code=POST, payload=payload, uri="coap://localhost/measurements")
    response = await context.request(request).response

    # print('Result: %s\n%r'%(response.code, response.payload))

if __name__ == "__main__":
    asyncio.run(main())
