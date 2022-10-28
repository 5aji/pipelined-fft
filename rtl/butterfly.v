// Butterfly transform (radix-2)
// Saji Champlin
// This module implements the DFT for the radix-2 case, often called a Butterfly Transform.
// 
// Since these are complex valued transformations, we split the parts into 
// real and imaginary components. We also have inputs for twiddle factors.


// The butterfly transform computes the following values:
// y0 = x0 + x1 * twiddle
// y1 = x0 - x1 * twiddle
//
// note that all of these variables are complex, having real and imaginary
// parts. we notate this with _re and _im respectively.
// This also makes non-trivial arithmetic more difficult, specifically
// multiplication. Note that multiplication of complex values is like this:
// (x + yi) (u + vi) = (xu - yv) + (xv + yu)i
// We implement this part in a separate module. This is because in hardware
// implementation, we may use special blocks on the FPGA to improve
// performance. See cplx_mul.v for a simple version for simulation.


module butterfly #(
	parameter WIDTH=16
) (
	input clk,
	input [WIDTH-1:0] a_re, a_im, b_re, b_im, twiddle_re, twiddle_im,
	output reg [WIDTH-1:0] y0_re, y0_im, y1_re, y1_im
);

// store multiplication terms.
wire [WIDTH-1:0] product_re, product_im;

// instantiate complex multiplier:
// calculates b * twiddle and stores in product
cplx_mul #(.WIDTH(WIDTH)) twiddle_mul (clk, b_re, b_im, twiddle_re, twiddle_im, product_re, product_im);
always @(*) begin // we don't clock this since it's just adders. Easy to synthesize combinationally.
	// the complex multiplier will act as our registers for our pipeline.
	// this can be confusing. Be careful when reasoning about it!
	y0_re = a_re + product_re;
	y0_im = a_im + product_im;
	
	y1_re = a_re - product_re;
	y1_im = a_im - product_im;
end

endmodule 

