import numpy as np
import struct
import pandas as pd
import beacontools
from beacontools import parse_packet
from converters import BinToFloat, BinToInt
from numpy import dtype
from bitstring import BitArray

test = b"5\x01\'\x02\xfd\x02/\x02e\x01%\xfd8\xc8Xn<\xc3"

print(BitArray(test).bin[:1])
def chunker(seq, size):
    return (seq[pos:pos + size] for pos in range(0, len(seq), size))

test = [16, -12, 1, 0, 3, 2, 999,0, -1277, -1, 1, 0]
# accelerom_string = b"".join([struct.pack("h", x) for x in test])
# print(b"".join([struct.pack("h", x) for x in test]))
def test_bin_float_converstion():
    val = 100
    test = struct.pack(">f", val)
    binary = float_to_bin(val)
    print(binary)
    print(BinToFloat().process(test))
    print(struct.unpack(">f", test))
    print(BinToFloat().process(test, True))
    print(struct.unpack("f", test))

def test_bin_int_converstion():
    val = 100
    test = struct.pack(">i", val)
    binary = float_to_bin(val)
    print(binary)
    print(BinToInt().process(test))
    print(struct.unpack(">i", test))
    print(BinToInt().process(test, True))
    print(struct.unpack("i", test))
    val = -100
    test = struct.pack(">i", val)
    binary = float_to_bin(val)
    print(binary)
    print(BinToInt().process(test))
    print(struct.unpack(">i", test))
    print(BinToInt().process(test, True))
    print(struct.unpack("i", test))


def float_to_bin(num):
    return format(struct.unpack('!I', struct.pack('!f', num))[0], '032b')


def convert_row_to_bytes(row):
    row = b"".join([struct.pack("h", x) for x in row])
    b2f = BinToFloat(15, 32)
    print([b2f.process(x) for x in chunker(row, 6)])

    # structure = "q"
    # i = 8
    # print(len(accelerom_string))
    # print(struct.unpack(structure, accelerom_string[:i]), struct.unpack(structure, accelerom_string[i:2*i]),
    #       struct.unpack(structure, accelerom_string[2*i:]))


data = pd.read_csv("accelerometer.data")
print(data)

test_bin_float_converstion()
test_bin_int_converstion()

# for index, row in data.iterrows():
#     convert_row_to_bytes(row)


