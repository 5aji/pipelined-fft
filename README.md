# pipelined-fft


This is the source code for my EE 5327 VLSI Design Lab Project. It is a pipelined FFT.

The test suite is done with cocotb, so we can use any verilog simulator we want.



## Generator scripts

Due to design complexity that exceeds "most" synthesis tools capabilities (requiring a lot of SystemVerilog support),
I instead wrote a generator program that takes in parameters about the desired FFT and creates a verilog module
that instantiates them all individually. This way, I can use python constructs to get more fine-tuned control
over the output HDL. Furthermore, we can use python to generate the twiddle factors needed for the specific FFT.


## Pipelining

A pipelined FFT is an FFT that can store different intermediate values after each stage of FFT.
A traditional FFT might have input lines that are clocked in once at the beginning, and stored internally
until the processing is finished (usually signaled with an out_ready flag or similar). In a pipelined FFT,
there is still a multi-cycle latency on the results of a particular input, but a new output is generated every
clock cycle. This is identical to how a pipelined CPU works. However, most FFT implementations that aren't
pipelined still take multiple clocks to execute.


## Test suite

The test suite is written in Python using `cocotb`, a platform-agnostic testbench controller.
