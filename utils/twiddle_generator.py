# Twiddle factor ROM generator.
# Generates one rom file, contianing real and imaginary parts of the twiddle.
# Saji Champlin 2022
# Written for EE5327

import math
import argparse
def twiddle(n,k):
    inner = -2 * math.pi * k / n
    return (math.cos(inner), math.sin(inner))


# n is the number of inputs, being a power of two (512, 128, etc)


def make_array(n):
    # compute the array of all twiddle factors for an n-input system.
    # this works because they are cyclic. 
    val_pairs = [twiddle(n,x) for x in range(n)]

    return val_pairs

def float_to_fixed_binary(num, n_bits, frac_point):
    # convert a floating point number to a binary string with 2's complement.
    # with n total bits, and m fraction bits.
    if frac_point >= n_bits - 1:
        print("ERROR: fraction bits greater than total bits")
        return "blah"
    result = int(num * (2 ** frac_point))
    if num < 0:
        # 2s complement it. with a bitwise and of 0b11111 equal to n_bits.
        result = result & ((2 ** n_bits) -1)
    return f'{result:0{n_bits}b}'


def fixed_binary_to_float(binstr, n_bits, frac_point):
    assert len(binstr) == n_bits, "binary string provided does not match expected number of bits"
    # do the reverse of the above.
    num = int(binstr, 2)
    if binstr[0] == '1': # negative
        num = num - (1 << n_bits) # reverse the twos complement.
    # handle fraction point.
    num = float(num) / (2 ** frac_point)
    return num 

def create_memory(data, n_bits, frac_point):
    # write the memory file.
    els = []
    for _,elem in enumerate(data):
        binstr = float_to_fixed_binary(elem, n_bits, frac_point)
        els.append(binstr)
    return els


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-b", "--num_bits", type=int, help="Total width of twiddle factors", default=16)
    parser.add_argument("-f", "--fraction_point", type=int, help="Number of bits to use for fraction", default=8)
    parser.add_argument("num_twiddles", metavar="N", type=int, help="Number of twiddle factors to generate", default=8)
    parser.add_argument("-o", "--output", type=argparse.FileType('w'), help="Where to store the result")
    
    args = parser.parse_args()
    arr = make_array(args.num_twiddles)
    arr = [item for tup in arr for item in tup]
    out = create_memory(arr,args.num_bits, args.fraction_point)
    if args.output:
        args.output.write('\n'.join(out))
    else:
        print('\n'.join(out))


