// Basic Core FFT verilog file.
// Saji Champlin 2022
// Written for EE 5323

// this file contains a manually-instantiated 8-input FFT. This means we don't
// use generate blocks, or block memory, or parameters. That will come later.
// Instead, this will be used as an end-to-end test that the fft primitives
// and constructs are functioning.


module basic_fft8(
	input clk,
	input [15:0] x_re [7:0], // x is a 1d array of 8 elements, each 16 bit
	input [15:0] x_im [7:0],
	output [15:0] y_re [7:0],
	output [15:0] y_im [7:0]
);

// intermediate value wires.
// with N=8, we have 3 layers. last one is output layer. first one is input, 
// so only 2 intermediate layers.
wire [15:0] inter_re [7:0][1:0]; // 2d array of 16-bit values.
wire [15:0] inter_im [7:0][1:0]; // 2d array of 16-bit values.

// twiddles.
// 8 values, real-im-real-im, 4 pairs repeating.

reg [15:0] tw_f [7:0];



// 1st stage, adjacent inputs get butterflied.

genvar i;
generate for (i = 0; i < 3; i = i + 1 ) begin
	butterfly bf_layer1(clk, 
		x_re[2 * i], x_im[2 * i], x_re[2*i+1],x_im[2*i+1], 
		tw_f[0], tw_f[0], 
		inter_re[2*i][0], inter_im[2*i][0], inter_re[2*i+1][0], inter_im[2*i+1][0]
	);
end
endgenerate



endmodule;
