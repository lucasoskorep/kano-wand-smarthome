import struct
from bitstring import BitArray
test = b"5\x01\'\x02\xfd\x02/\x02e\x01%\xfd8\xc8Xn<\xc3"
# test = b'\x0f\x00'
# print(len(test))
# first = test[:4]
#
# last = test[14:]
#

print(BitArray(test).bin[:1])