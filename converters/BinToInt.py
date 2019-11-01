from bitstring import BitArray


def chunker(seq, size):
    return (seq[pos:pos + size] for pos in range(0, len(seq), size))


class BinToInt(object):

    def __init__(self, size = 32, signed=True):
        self.signed = signed

    def process(self, bin_string, reverse_marshalling=False):
        var = BitArray(bin_string)
        print(bin_string)
        chunked_bytes = [x for x in chunker(var, 8)]
        ordered_bytes = []
        for group in reversed(chunked_bytes) if reverse_marshalling else chunked_bytes:
            ordered_bytes.extend(group)
        ordered_bytes = [not x for x in reversed(ordered_bytes)]
        # print(
        #     "".join(["1" if x else "0" for x in ordered_bytes[0:1]]),
        #     "".join(["1" if x else "0" for x in ordered_bytes[1:1+self.exponent]]),
        #     "".join(["1" if x else "0" for x in ordered_bytes[1+self.exponent:1+self.exponent+self.mantissa]])
        # )
        # sign =
        # return -val if sign else val

        print([1 if x else 0 for x in ordered_bytes[:-1]])
        if self.signed:
            return self.convert_pos_int(ordered_bytes[:-1]) * (1 if False else -1)
        else:
            return self.convert_pos_int(ordered_bytes)

    def convert_pos_int(self, val):
        total_val = 0
        digit_val = 1
        for i in val:
            total_val += digit_val if i else 0
            digit_val *= 2
        return total_val
