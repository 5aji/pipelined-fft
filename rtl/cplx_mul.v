// Verilog complex number multiplier
// Saji Champlin 2022
// Written for EE 5323

// This module is a simple complex multiplier. It assumes that the toolchain
// can synthesize 1-clock multipliers. If this doesn't work, a different
// module will be needed instead.
module cplx_mul #(
	parameter WIDTH=16,
	parameter FIXED_POINT=8
) (
	input clk,
	input signed [WIDTH-1:0] a_re, a_im, b_re, b_im,
	output signed [WIDTH-1:0] y0_re, y0_im
);

reg signed [2*WIDTH - 1:0] res_re, res_im;


// the shifted 1 by fixed point -1 is for rounding.
localparam ROUND_FACTOR = 1 << (FIXED_POINT -1);
assign y0_re = res_re[FIXED_POINT + WIDTH-1:FIXED_POINT];
assign y0_im = res_im[FIXED_POINT + WIDTH-1:FIXED_POINT];
always @(posedge clk) begin
	res_re <= a_re * b_re - a_im * b_im + ROUND_FACTOR;
	res_im <= a_re * b_im + a_im * b_re + ROUND_FACTOR;
end
endmodule

