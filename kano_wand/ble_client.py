import logging

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

    async def connect_and_read(self, debug=False):
        if debug:
            import sys
            l = logging.getLogger("asyncio")
            l.setLevel(logging.DEBUG)
            h = logging.StreamHandler(sys.stdout)
            h.setLevel(logging.DEBUG)
            l.addHandler(h)
            logger.addHandler(h)

        async with BleakClient(self.wand_address, loop=self.loop) as client:
            self.client = client
            x = await client.is_connected()
            logger.info("Connected: {0}".format(x))
            await start_notify(self.client, self.sensor_handling)


    async def stop_recieving_data(self):
        await stop_notify(self.client)


    def sensor_update_handler(self, sensors):
        print(sensors)

    def sensor_handling(self, sender, data):
        """Simple notification handler which prints the data received."""
        sender = CHARACTERISTIC_UUIDS[sender]
        if sender == BUTTON:
            self.wand_sensors.set_button(self.decoder.decode_button(data))
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
