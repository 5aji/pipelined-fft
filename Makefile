# Makefile

# defaults
SIM ?= icarus
TOPLEVEL_LANG ?= verilog

VERILOG_SOURCES += rtl/butterfly.v rtl/cplx_mul.v rtl/fft.v
# use VHDL_SOURCES for VHDL files

# TOPLEVEL is the name of the toplevel module in your Verilog or VHDL file
TOPLEVEL = basic_fft8

# MODULE is the basename of the Python test file
MODULE = tests.test_design

all:
	$(MAKE) clean
	$(MAKE) cplx_tests
	$(MAKE) clean
	$(MAKE) butterfly_tests
	$(MAKE) clean
	$(MAKE) sim

cplx_tests: #unit tests for the complex multiplication unit
	$(MAKE) sim MODULE=tests.test_cplx_mul TOPLEVEL=cplx_mul
butterfly_tests:
	$(MAKE) sim MODULE=tests.test_butterfly TOPLEVEL=butterfly


# include cocotb's make rules to take care of the simulator setup
include $(shell cocotb-config --makefiles)/Makefile.sim
