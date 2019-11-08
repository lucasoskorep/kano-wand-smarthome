import logging
import asyncio
import platform
import struct
import time
import pandas as pd

from bleak import BleakClient
from bleak import _logger as logger
from converters import BinToInt, BinToFloat

"""
This is used for reading and decoding values from t he Kano Harry Potter Coding Wand
- Wand sends 25 updates to gyro and accel every second
- Wand sends 3 Dimensional data as 48 bit reverse marshalled integers
- Wand seems to send smaller single dimensional data in 16bit unsigned integers 
"""

BUTTON = 1
NINE_AXIS = 2
ACCELEROMETER = 3
BATTERY = 4
TEMPERATURE = 5
MAGNETOMETER = 6

INT_DECODER = BinToInt(48)
FLOAT_DECODER = BinToFloat(16, 31)
BUTTON_STATUS = None

CHARACTERISTIC_UUIDS = {
    ("64a7000d-f691-4b93-a6f4-0968f5b648f8"): BUTTON,  # Button
    ("64a7000a-f691-4b93-a6f4-0968f5b648f8"): NINE_AXIS,  # 9 axis
    ("64a7000c-f691-4b93-a6f4-0968f5b648f8"): ACCELEROMETER,  # Accel
    # ("64a70007-f691-4b93-a6f4-0968f5b648f8"):BATTERY,
    # ("64a70014-f691-4b93-a6f4-0968f5b648f8"):TEMPERATURE,
    # ("64a70014-f691-4b93-a6f4-0968f5b648f8"):MAGNETOMETER
}  # <--- Change to the characteristic you want to enable notifications from.

# TODO: RUMBLE
# TODO: RGB

device_address = "D8:9B:12:D1:08:80"


class Gyro(object):
    def __init__(self):
        self.x = 0
        self.y = 0
        self.z = 0

    def __str__(self):
        print(self.x, self.y, self.z)


class Accel(object):
    def __init__(self):
        self.x = 0
        self.y = 0
        self.z = 0

    def __str__(self):
        print(self.x, self.y, self.z)


class Sensors(object):
    def __init__(self):
        self.gyro = None
        self.gyro_updates = 0

        self.accel = None
        self.accel_updates = 0
        self.dataframe = pd.DataFrame(columns=["gyro_x", "gyro_y", "gyro_z", "accel_x", "accel_y", "accel_z"])

    def append_to_dataframe(self):
        # print("Printing the gyro and accel", self.gyro, self.accel)
        # print(self.dataframe)
        # print(self.gyro_updates, self.accel_updates)
        if self.gyro_updates == self.accel_updates:
            # print({
            #     "gyro_x": self.gyro.x,
            #     "gyro_y": self.gyro.y,
            #     "gyro_z": self.gyro.z,
            #     "accel_x": self.accel.x,
            #     "accel_y": self.accel.y,
            #     "accel_z": self.accel.z,
            # })
            # try:
            #
            # except Exception as e:
            #     print("ERROR HAS OCCURRED")
            #     print(e)
            self.dataframe = self.dataframe.append(
                pd.DataFrame({
                    "gyro_x": self.gyro.x,
                    "gyro_y": self.gyro.y,
                    "gyro_z": self.gyro.z,
                    "accel_x": self.accel.x,
                    "accel_y": self.accel.y,
                    "accel_z": self.accel.z,
                }, index=[0])
            )

    def save_df_to_file(self, filename):
        self.dataframe.to_csv(filename, index=False)

    def set_gyro(self, gyro):
        self.gyro = gyro
        self.gyro_updates += 1

    def set_accel(self, accel):
        self.accel = accel
        self.accel_updates += 1


def chunker(seq, size):
    return (seq[pos:pos + size] for pos in range(0, len(seq), size))


count = 0


def decode_button(data):
    global sensors, count
    if int.from_bytes(data, byteorder='big'):
        print("Button Pressed")
        sensors = Sensors()
        count += 1
    else:
        print("Button Released")
        sensors.save_df_to_file(f"dataset{count}.csv")


def decode_nine_axis(data):
    converted = [INT_DECODER.process(x, True) / 10 ** 14 for x in chunker(data, 6)]

    # print(converted, sum(converted))
    return converted


def decode_accelerometer(data):
    converted = [INT_DECODER.process(x, True) / 10 ** 14 for x in chunker(data, 6)]
    # print(converted, sum(converted))
    return converted


def decode_battery(data):
    global BUTTON_STATUS
    BUTTON_STATUS = int.from_bytes(data, byteorder='big')


def decode_temp(data):
    print(len(data))
    print(data)
    print(struct.unpack("h", data))


def decode_magnet(data):
    print(data)
    print(len(data))


count = 0

sensors = Sensors()


def notification_handler(sender, data):
    global count, sensors
    """Simple notification handler which prints the data received."""
    # TODO: Convert to a dictionary and a single decode command
    sender = CHARACTERISTIC_UUIDS[sender]
    if sender == BUTTON:
        decode_button(data)
    elif sender == NINE_AXIS:
        gyro = Gyro()
        # print("getting gyro values")

        gyro.x, gyro.y, gyro.z = decode_nine_axis(data)
        # print("got gyro values")
        # print(gyro)
        sensors.set_gyro(gyro)
        sensors.append_to_dataframe()
    elif sender == ACCELEROMETER:
        accel = Accel()
        accel.x, accel.y, accel.z = decode_nine_axis(data)
        sensors.set_accel(accel)
        sensors.append_to_dataframe()
        # decode_accelerometer(data)
    elif sender == BATTERY:
        decode_battery(data)
    elif sender == TEMPERATURE:
        decode_temp(data)
    elif sender == MAGNETOMETER:
        decode_magnet(data)


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

        # await asyncio.sleep(60.0, loop=loop)
        while True:
            time.sleep(1)

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
