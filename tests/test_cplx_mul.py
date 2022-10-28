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

def trunc(num, bits, f_point):
    # a helper that eliminates floating precision that we don't have with fixed point.
    return b2fl(fl2b(num, bits, f_point), bits, f_point)


async def set_terms(dut, cplx_a, cplx_b):
    # set the values of the multiplier based on two complex numbers.
    dut.a_re.value = int(fl2b(cplx_a.real,16,8),2)
    dut.a_im.value = int(fl2b(cplx_a.imag,16,8),2)
    dut.b_re.value = int(fl2b(cplx_b.real,16,8),2)
    dut.b_im.value = int(fl2b(cplx_b.imag,16,8),2)

async def get_product(dut):
    # get the product from the DUT
    re = b2fl(str(dut.y0_re.value), 16,8)
    imag = b2fl(str(dut.y0_im.value), 16,8)
    return re + 1j * imag

@cocotb.test()
async def test_unity(dut):
    cocotb.start_soon(Clock(dut.clk, 1, 'ns').start())
    await RisingEdge(dut.clk)

    num1 = random.uniform(-4,4)
    # num2 = random.uniform(-4,4)
    num2 = 2
    await set_terms(dut, num1, num2)

    await RisingEdge(dut.clk)
    await ReadWrite()
    res = await get_product(dut)
    expected_val = trunc(num1, 16,8) * trunc(num2,16,8)

    assert res.real == expected_val
    
@cocotb.test()
async def test_negation(dut):
    cocotb.start_soon(Clock(dut.clk, 1, 'ns').start())

    num1 = random.uniform(-4,4)
    # num2 = random.uniform(-4,4)
    num2 = -1
    await set_terms(dut, num1,num2)

    await RisingEdge(dut.clk)
    await ReadWrite()
    res = await get_product(dut)
    expected_val = trunc(num1, 16,8) * trunc(num2,16,8)
    assert res.real == expected_val

@cocotb.test()
async def test_imag(dut):
    cocotb.start_soon(Clock(dut.clk, 1, 'ns').start())

    await set_terms(dut, 1j, 1j)

    await RisingEdge(dut.clk)
    await ReadWrite()
    res = await get_product(dut)
    assert res.real == -1


@cocotb.test()
async def test_cplx(dut):
    cocotb.start_soon(Clock(dut.clk, 1, 'ns').start())

    await set_terms(dut, 2 + 1j, 3 + 4j)
    await RisingEdge(dut.clk)
    await ReadWrite()
    res = await get_product(dut)
    assert res == 2 + 11j


@cocotb.test()
async def test_rand_ints(dut):
    cocotb.start_soon(Clock(dut.clk, 1, 'ns').start())

    for _ in range(100):
        n1_re = random.randint(-8,8)
        n1_im = random.randint(-8,8)
        n2_re = random.randint(-8,8)
        n2_im = random.randint(-8,8)
        n1 = n1_re + 1j * n1_im
        n2 = n2_re + 1j * n2_im
        await set_terms(dut, n1, n2)
        await RisingEdge(dut.clk)
        await ReadWrite()
        res = await get_product(dut)
        assert res == n1 * n2


@cocotb.test()
async def test_rand_floats(dut):
    cocotb.start_soon(Clock(dut.clk, 1, 'ns').start())

    for _ in range(1000):
        n1_re = trunc(random.uniform(-8,8), 16,8)
        n1_im = trunc(random.uniform(-8,8), 16,8)
        n2_re = trunc(random.uniform(-8,8), 16,8)
        n2_im = trunc(random.uniform(-8,8), 16,8)
        n1 = n1_re + 1j * n1_im
        n2 = n2_re + 1j * n2_im
        await set_terms(dut, n1, n2)
        await RisingEdge(dut.clk)
        await ReadWrite()
        res = await get_product(dut)
        expected = n1 * n2
        assert math.isclose(res.real,expected.real, abs_tol=0.00390625)
        assert math.isclose(res.imag,expected.imag, abs_tol=0.00390625)




