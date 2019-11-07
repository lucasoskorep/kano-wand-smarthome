from bitstring import BitArray


def chunker(seq, size):
    return (seq[pos:pos + size] for pos in range(0, len(seq), size))


class BinToInt(object):

    def __init__(self, size = 32, signed=True):
        self.signed = signed

    def process(self, bin_string, reverse_marshalling=False):
        var = BitArray(bin_string)
        chunked_bytes = [x for x in chunker(var, 8)]
        ordered_bytes = []
        for group in chunked_bytes if reverse_marshalling else reversed(chunked_bytes):
            ordered_bytes.extend(group)
        ordered_bytes = [x for x in reversed(ordered_bytes)]

        if self.signed:
            negative = ordered_bytes[-1]
        else:
            negative = False

        # print([1 if x else 0 for x in ordered_bytes[:]])
        if self.signed:
            return self.convert_pos_int(ordered_bytes[:], negative)
        else:
            return self.convert_pos_int(ordered_bytes)

    def convert_unsigned_int(self, val):
        total_val = 0
        digit_val = 1
        for i in val:
            total_val += digit_val if i else 0
            digit_val *= 2
        return total_val

    def convert_pos_int(self, val, negative):
        if negative:
            val = [not x for x in val]
            self.add_one_to_binary_int(val)
        return self.convert_unsigned_int(val) * (-1 if negative else 1)

    def add_one_to_binary_int(self, binary_list):
        for i in range(len(binary_list)):
            if binary_list[i]:
                binary_list[i] = 0
            else:
                binary_list[i] = 1
                break
