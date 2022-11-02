// bit reversal module
// saji champlin 2022
// written for EE 5323

// the cooley-tukey FFT algorithm requires that you reorder the inputs
// in a specific manner before processing them.

module bit_reorder #(
	parameter WIDTH=16
) (
	input signed [WIDTH-1:0] a [7:0],
	output signed [WIDTH-1:0] y [7:0]
);

assign y[0] = a[0];
assign y[1] = a[4];
assign y[2] = a[2];
assign y[3] = a[6];
assign y[4] = a[1];
assign y[5] = a[5];
assign y[6] = a[3];
assign y[7] = a[7];


endmodule


