import logging
import struct

from converters import BinToInt, BinToFloat
from .sensor_tracker import *
from bleak import BleakClient
from bleak import _logger as logger
from .utils import *

class KanoBLEClient(object):
    def __init__(self, wand_address, spells=None):
        self.wand_address = wand_address
        self.int_decoder = BinToInt(48)
        self.float_decoder = BinToFloat(16, 31)
        self.client = None


    async def connect(self, loop, debug=False):
        if debug:
            import sys
            l = logging.getLogger("asyncio")
            l.setLevel(logging.DEBUG)
            h = logging.StreamHandler(sys.stdout)
            h.setLevel(logging.DEBUG)
            l.addHandler(h)
            logger.addHandler(h)

        async with BleakClient(self.wand_address, loop=loop) as client:
            self.client = client
            x = await client.is_connected()
            logger.info("Connected: {0}".format(x))

    async def start_recieving_data(self):
        await start_notify(self.client)


    async def stop_recieving_data(self):
        await stop_notify(self.client)


    def sensor_handling(self, sender, data):
        """Simple notification handler which prints the data received."""
        # TODO: Convert to a dictionary and a single decode command
        sender = CHARACTERISTIC_UUIDS[sender]
        if sender == BUTTON:
            self.decode_button(data)
        elif sender == NINE_AXIS:
            #TODO: refactor the gyro to be local to the sensors file only
            gyro = Gyro()
            gyro.x, gyro.y, gyro.z = self.decode_nine_axis(data)
            sensors.set_gyro(gyro)
            sensors.append_to_dataframe()
        elif sender == ACCELEROMETER:
            accel = Accel()
            accel.x, accel.y, accel.z = self.decode_nine_axis(data)
            sensors.set_accel(accel)
            sensors.append_to_dataframe()
        elif sender == BATTERY:
            self.decode_battery(data)
        elif sender == TEMPERATURE:
            self.decode_temp(data)
        elif sender == MAGNETOMETER:
            self.decode_magnet(data)

