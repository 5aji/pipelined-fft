import cocotb
from cocotb.triggers import Timer

@cocotb.test()
async def test_test(dut):
    for cycle in range(10):
        dut.clk.value = 0
        await Timer(1,units="ns")
        dut.clk.value = 1
        await Timer(1,units="ns")
    dut._log.info("this is an EOF log")

