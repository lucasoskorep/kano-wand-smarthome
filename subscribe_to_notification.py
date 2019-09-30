"""
Notifications
-------------
Example showing how to add notifications to a characteristic and handle the responses.
Updated on 2019-07-03 by hbldh <henrik.blidh@gmail.com>
"""

import logging
import asyncio
import platform
import struct

from bleak import BleakClient
from bleak import _logger as logger
from bitstring import BitArray
from struct import Struct
BUTTON = 1
GYROSCOPE = 2
ACCELEROMETER = 3
BATTERY = 4
TEMPERATURE = 5

CHARACTERISTIC_UUIDS = {
    # ("64a7000d-f691-4b93-a6f4-0968f5b648f8"):BUTTON,#Button
    # ("64a7000a-f691-4b93-a6f4-0968f5b648f8"):GYROSCOPE,#9 axis
    ("64a7000c-f691-4b93-a6f4-0968f5b648f8"): ACCELEROMETER,  # Accel
    # ("64a70007-f691-4b93-a6f4-0968f5b648f8"):BATTERY,
    # ("64a70014-f691-4b93-a6f4-0968f5b648f8"):TEMPERATURE
# Accel
}  # <--- Change to the characteristic you want to enable notifications from.

# device_address = "e3:ae:cd:af:28:e2"
device_address = "D8:9B:12:D1:08:80"

def decode_button(data):
    print(data)
    print(int.from_bytes(data, byteorder='big'))

def decode_accelerometer(data):
    # print(data)
    # print(len(data))
    print([x for x in data])
    print(int.from_bytes())

def decode_battery(data):
    print(len(data))
    print(data)
    print(int.from_bytes(data, byteorder='big'))

def decode_temp(data):
    print(len(data))
    print(data)
    print(struct.unpack("h", data))


def notification_handler(sender, data):
    """Simple notification handler which prints the data received."""
    sender = CHARACTERISTIC_UUIDS[sender]
    if sender == BUTTON:
        print(f"BUTTON PRESSED {data}")
        decode_button(data)
    elif sender == GYROSCOPE:
        # print(f"GYRO CHANGED - {data}")
        print(BitArray(data).bin[:1])
    elif sender == ACCELEROMETER:
        # print(f"ACCEL CHANGED - {data}")
        # print(BitArray(data).bin[:1])
        # print(struct.unpack("h",data[:2]))
        s = Struct("h")
        print([x for x in s.iter_unpack(data)])
        # print(struct.unpack("e",data[:2]))
        # print(struct.unpack("f", data[:4]))

        # decode_accelerometer(data)
    elif sender == BATTERY:
        decode_battery(data)
    elif sender == TEMPERATURE:
        decode_temp(data)


async def start_notify(client):
    for char in CHARACTERISTIC_UUIDS.keys():
        await client.start_notify(char, notification_handler)

async def stop_notify(client):
    for char in CHARACTERISTIC_UUIDS.keys():
        await client.stop_notify(char)

async def run(address, loop, debug=False):
    if debug:
        import sys

        # loop.set_debug(True)
        l = logging.getLogger("asyncio")
        l.setLevel(logging.DEBUG)
        h = logging.StreamHandler(sys.stdout)
        h.setLevel(logging.DEBUG)
        l.addHandler(h)
        logger.addHandler(h)

    async with BleakClient(address, loop=loop) as client:
        x = await client.is_connected()
        logger.info("Connected: {0}".format(x))
        await start_notify(client)
        await asyncio.sleep(60.0, loop=loop)
        await stop_notify(client)


if __name__ == "__main__":
    import os

    os.environ["PYTHONASYNCIODEBUG"] = str(1)
    address = (
        device_address  # <--- Change to your device's address here if you are using Windows or Linux
        if platform.system() != "Darwin"
        else "243E23AE-4A99-406C-B317-18F1BD7B4CBE"  # <--- Change to your device's address here if you are using macOS
    )
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run(address, loop, True))