import logging
import struct

from time import sleep
from converters import BinToInt, BinToFloat
from .wand_sensors import *
from bleak import BleakClient
from bleak import _logger as logger
from .wand_utils import *
from .sensor_decoders import wand_decoder


class KanoBLEClient(object):
    def __init__(self, wand_address, loop, spells=None):
        self.wand_address = wand_address
        self.int_decoder = BinToInt(48)
        self.float_decoder = BinToFloat(16, 31)
        self.client = None
        self.decoder = wand_decoder()
        self.wand_sensors = WandSensors(self.sensor_update_handler)
        self.loop = loop
        self.dateframe_handler = None

    async def connect(self, debug=False):
        if debug:
            import sys
            l = logging.getLogger("asyncio")
            l.setLevel(logging.DEBUG)
            h = logging.StreamHandler(sys.stdout)
            h.setLevel(logging.DEBUG)
            l.addHandler(h)
            logger.addHandler(h)

        self.client = BleakClient(self.wand_address, loop=self.loop)
        await self.client.connect()
        x = await self.client.is_connected()
        logger.info("Connected: {0}".format(x))


    async def start_recieving_data(self, sensors=None):
        await start_notify(self.client, self.sensor_handling, sensors)

    async def stop_recieving_data(self, sensors):
        await stop_notify(self.client, sensors)

    def change_spell(self, spell):
        self.wand_sensors.data_folder = "./training_data/" + spell + "/"
        print(f"changed wand folder to {self.wand_sensors.data_folder}")

    def sensor_update_handler(self, sensors):
        print(sensors)
        # print("SENSORS RECIEVED")
        return


    def sensor_handling(self, sender, data):
        """Simple notification handler which prints the data received."""
        sender = get_key(sender, CHARACTERISTIC_UUIDS)
        if sender == BUTTON:
            self.wand_sensors.set_button(self.decoder.decode_button(data))
            self.loop.run_until_complete(self.client.write_gatt_char(RESET_CHAR, struct.pack("h", 1)))
        elif sender == NINE_AXIS:
            self.wand_sensors.set_gyro(*self.decoder.decode_nine_axis(data))
        elif sender == ACCELEROMETER:
            self.wand_sensors.set_accel(*self.decoder.decode_nine_axis(data))
        elif sender == BATTERY:
            self.decoder.decode_battery(data)
        elif sender == TEMPERATURE:
            self.wand_sensors.set_temp(self.decoder.decode_temp(data))
        elif sender == MAGNETOMETER:
            self.wand_sensors.set_magneto(self.decoder.decode_magnet(data))
