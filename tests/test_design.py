import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, ReadWrite, ClockCycles
import random
import sys
import math
import numpy as np
sys.path.append(".")
from utils import twiddle_generator as tw

fl2b = tw.float_to_fixed_binary
b2fl = tw.fixed_binary_to_float

def trunc(num, bits=16, f_point=8):
    # a helper that eliminates floating precision that we don't have with fixed point.
    return b2fl(fl2b(num, bits, f_point), bits, f_point)


async def set_inputs(dut, x):
    dut.x_re.value = [int(fl2b(a.real,16,8),2) for a in x]
    dut.x_im.value = [int(fl2b(a.imag,16,8),2) for a in x]

def convert_array(arr):
    return [b2fl(str(a), 16,8) for a in arr]



@cocotb.test()
async def test_twiddle_mem(dut):
    await ReadWrite()
    v = dut.tw_f.value
    cor = tw.make_array(8)
    cor = [fl2b(item,16,8) for tup in cor for item in tup]
    for idx in range(0,len(v), 2):
        im = str(v[idx+1])
        re = str(v[idx])
        assert cor[idx] == re
        assert cor[idx + 1] == im




@cocotb.test()
async def test_zeros(dut):
    cocotb.start_soon(Clock(dut.clk, 1, 'ns').start())
    x = [0] * 8
    await set_inputs(dut, x)

    await ClockCycles(dut.clk, 3)
    await ReadWrite()
    assert all([f == 0 for f in dut.y_re.value])
    assert all([f == 0 for f in dut.y_im.value])


@cocotb.test()
async def test_fixed(dut):
    cocotb.start_soon(Clock(dut.clk, 1, 'ns').start())
    # x = [1,0,1,0,1,0,1,0]
    # x = [1,0,-1,0,1,0,-1,0]
    x = [1,1,1,1,0,0,0,0]
    await set_inputs(dut, x)

    await ClockCycles(dut.clk, 4)
    await ReadWrite()
    print(dut.x_re.value)
    y_re = np.array(convert_array(dut.y_re.value))
    y_im = np.array(convert_array(dut.y_im.value))
    y = y_re + 1j * y_im
    print(y)
    print(np.fft.fft(x))


