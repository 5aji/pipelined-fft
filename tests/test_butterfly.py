import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, ReadWrite
import random
import sys
import math
sys.path.append(".")
from utils import twiddle_generator as tw

fl2b = tw.float_to_fixed_binary
b2fl = tw.fixed_binary_to_float

def trunc(num, bits=16, f_point=8):
    # a helper that eliminates floating precision that we don't have with fixed point.
    return b2fl(fl2b(num, bits, f_point), bits, f_point)

# a helper that generates a random, truncated complex number.

# Helpers to set and get the values from the radix-2 butterfly.
async def set_inputs(dut, a,b,twiddle):
    dut.a_re.value = int(fl2b(a.real,16,8),2)
    dut.a_im.value = int(fl2b(a.imag,16,8),2)
    dut.b_re.value = int(fl2b(b.real,16,8),2)
    dut.b_im.value = int(fl2b(b.imag,16,8),2)
    dut.twiddle_re.value = int(fl2b(twiddle.real,16,8),2)
    dut.twiddle_im.value = int(fl2b(twiddle.imag,16,8),2)

async def get_outputs(dut):
    y0 = b2fl(str(dut.y0_re.value), 16,8) + 1j * b2fl(str(dut.y0_im.value), 16,8)
    y1 = b2fl(str(dut.y1_re.value), 16,8) + 1j * b2fl(str(dut.y1_im.value), 16,8)
    return y0,y1

async def cplx_close(a,b, **kwargs):
    r1 = math.isclose(a.real, b.real, **kwargs)
    r2 = math.isclose(a.imag, b.imag, **kwargs)
    return r1 and r2

@cocotb.test()
async def test_fixed(dut):
    cocotb.start_soon(Clock(dut.clk, 1, 'ns').start())
    a = 2 + 3j
    b = -1.5 + -4j
    twiddle = 0.707 + 0j
    await set_inputs(dut, a,b,twiddle)

    await RisingEdge(dut.clk)
    await ReadWrite()

    y0, y1 = await get_outputs(dut)

    assert await cplx_close(y0,a + b * twiddle, abs_tol=4*0.00390625)
    assert await cplx_close(y1,a - b * twiddle, abs_tol=4*0.00390625)


async def random_cplx(a,b):
    return trunc(random.uniform(a,b)) + 1j * trunc(random.uniform(a,b))

@cocotb.test()
async def test_random(dut):
    cocotb.start_soon(Clock(dut.clk, 1, 'ns').start())

    for _ in range(1000):
        a = await random_cplx(-8,8)
        b = await random_cplx(-8,8)
        twiddle = tw.twiddle(128, random.randrange(128))
        twiddle = trunc(twiddle[0]) + 1j * trunc(twiddle[1])
        await set_inputs(dut, a,b,twiddle)

        await RisingEdge(dut.clk)
        await ReadWrite()

        y0, y1 = await get_outputs(dut)

        assert await cplx_close(y0,a + b * twiddle, abs_tol=4*0.00390625)
        assert await cplx_close(y1,a - b * twiddle, abs_tol=4*0.00390625)
