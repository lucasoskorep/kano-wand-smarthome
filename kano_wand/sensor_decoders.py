import struct
from .wand_utils import chunker
from converters import BinToInt, BinToFloat

class wand_decoder(object):
    def __init__(self, int_decoder=BinToInt(48), float_decoder= BinToFloat(16, 31)):
        self.int_decoder = int_decoder
        self.float_decoder = float_decoder

    def decode_button(self, data):
        return int.from_bytes(data, byteorder='big')

    def decode_nine_axis(self, data):
        converted = [self.int_decoder.process(x, True) / 10 ** 14 for x in chunker(data, 6)]
        return converted

    def decode_accelerometer(self, data):
        converted = [self.int_decoder.process(x, True) / 10 ** 14 for x in chunker(data, 6)]
        return converted

    def decode_battery(self, data):
        return int.from_bytes(data, byteorder='big')

    def decode_temp(self, data):
        return struct.unpack("h", data)

    def decode_magnet(self, data):
        print(data)
        print(len(data))
        return 0
