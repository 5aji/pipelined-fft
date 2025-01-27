// Basic Core FFT verilog file.
// Saji Champlin 2022
// Written for EE 5323

// this file contains a manually-instantiated 8-input FFT. This means we don't
// use generate blocks, or block memory, or parameters. That will come later.
// Instead, this will be used as an end-to-end test that the fft primitives
// and constructs are functioning.


module basic_fft8(
	input clk,
	input signed [15:0] x_re [7:0], // x is a 1d array of 8 elements, each 16 bit
	input signed [15:0] x_im [7:0],
	output signed [15:0] y_re [7:0],
	output signed [15:0] y_im [7:0]
);

// intermediate value wires.
// with N=8, we have 3 layers. last one is output layer. first one is input, 
// so only 2 intermediate layers.
wire signed [15:0] inter_re_0 [7:0]; 
wire signed [15:0] inter_im_0 [7:0]; 
wire signed [15:0] inter_re_1 [7:0]; 
wire signed [15:0] inter_im_1 [7:0]; 

// bit-reversal
wire signed [15:0] rev_re [7:0];
wire signed [15:0] rev_im [7:0];
bit_reorder re_reorder(x_re, rev_re);
bit_reorder im_reorder(x_im, rev_im);

// twiddles.
// 8 values, real-im-real-im, 4 pairs repeating.

reg signed [15:0] tw_f [0:15];
initial $readmemb("rtl/fft8.mem", tw_f);

// 1st stage, adjacent inputs get butterflied.

genvar i;
generate for (i = 0; i < 4; i = i + 1 ) begin
	butterfly bf_layer1(clk, 
		rev_re[2 * i], rev_im[2 * i], rev_re[2*i+1],rev_im[2*i+1], 
		tw_f[0], tw_f[1], 
		inter_re_0[2*i], inter_im_0[2*i], inter_re_0[2*i+1], inter_im_0[2*i+1]
	);
end
endgenerate

// 2nd stage.

generate for (i = 0; i < 2; i = i + 1) begin
	butterfly bf1_layer2(clk,
		inter_re_0[4 * i], inter_im_0[4*i],
		inter_re_0[4*i+2], inter_im_0[4*i+2],
		tw_f[0], tw_f[1],
		inter_re_1[4 * i], inter_im_1[4*i],
		inter_re_1[4*i+2], inter_im_1[4*i+2]
	);
	butterfly bf2_layer2(clk,
		inter_re_0[4*i+1], inter_im_0[4*i+1],
		inter_re_0[4*i+3], inter_im_0[4*i+3],
		tw_f[4], tw_f[5],
		inter_re_1[4*i+1], inter_im_1[4*i+1],
		inter_re_1[4*i+3], inter_im_1[4*i+3]
	);

end
endgenerate

// 3rd stage.
generate for (i = 0; i < 4; i = i + 1 ) begin
	butterfly bf_layer3(clk, 
		inter_re_1[i], inter_im_1[i],
		inter_re_1[i+4], inter_im_1[i+4],
		 
		tw_f[i], tw_f[i+1], 
		y_re[i], y_im[i], y_re[i+4], y_im[i+4]
	);
end
endgenerate


endmodule
