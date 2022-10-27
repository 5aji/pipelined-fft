// Verilog complex number multiplier
// Saji Champlin 2022
// Written for EE 5323

// This module is a simple complex multiplier. It assumes that the toolchain
// can synthesize 1-clock multipliers. If this doesn't work, a different
// module will be needed instead.
module cplx_mul #(
	parameter WIDTH=16
) (
	input clk,
	input [WIDTH-1:0] a_re, a_im, b_re, b_im,
	output reg [WIDTH-1:0] y0_re, y0_im
);

always @(posedge clk) begin
	y0_re <= a_re * b_re - a_im * b_im;
	y0_im <= a_re * b_im + a_im * b_re;
end
endmodule

