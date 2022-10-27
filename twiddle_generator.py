# Twiddle factor ROM generator.
# Generates one rom file, contianing real and imaginary parts of the twiddle.
# Saji Champlin 2022
# Written for EE5327

import math
import struct

def twiddle(n,k):
    inner = -2 * math.pi * k / n
    return (math.cos(inner), math.sin(inner))




# n is the number of inputs, being a power of two (512, 128, etc)


def make_array(n):
    # compute the array of all twiddle factors for an n-input system.
    val_pairs = [twiddle(n,x) for x in range(n)]

    return zip(*val_pairs)

def float_to_fixed_hex(num, n_bits, n_fraction_bits):
    # convert a floating point number to a binary string:
    # with n total bits, and m fraction bits.
    if n_fraction_bits >= n_bits - 1:
        print("ERROR: fraction bits greater than total bits")
        return "blah"
    result = int(num * 2 ** n_fraction_bits)
    return f'{result:0{n_bits}b}'


def write_memory(filename):
    # write the memory file.
    # needs some way for specifying precision/format
    with open(filename, "w") as f:
        pass

