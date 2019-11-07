from bitstring import BitArray


def chunker(seq, size):
    return (seq[pos:pos + size] for pos in range(0, len(seq), size))


class BinToFloat(object):

    def __init__(self, exponent=8, mantissa=23):
        self.signed = True
        self.exponent = exponent
        self.mantissa = mantissa
        self.tot_len = exponent + mantissa + (1 if self.signed else 0)

    def process(self, bin_string, reverse_marshalling=False):
        var = BitArray(bin_string)
        chunked_bytes = [x for x in chunker(var, 8)]
        ordered_bytes = []
        for group in reversed(chunked_bytes) if reverse_marshalling else chunked_bytes:
            ordered_bytes.extend(group)
        mant = [x for x in reversed(ordered_bytes[:self.mantissa])]
        exp = ordered_bytes[self.mantissa:self.mantissa + self.exponent]
        sign = ordered_bytes[self.mantissa + self.exponent] if self.signed else True
        exp = self.convert_exp(exp)
        mant = self.convert_mantissa(mant)
        val = 2.0 ** exp * mant
        return -val if sign else val

    def convert_exp(self, exp):
        total_val = 0
        digit_val = 1
        for i in exp:
            total_val += digit_val if i else 0
            digit_val *= 2
        tot = (2 ** (self.exponent-1))-1
        return total_val - (tot)

    def convert_mantissa(self, mant):
        total_val = 1
        digit_val = .5
        for i in mant:
            total_val += digit_val if i else 0
            digit_val /= 2
        return total_val
