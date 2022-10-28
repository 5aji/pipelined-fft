# Test suite for twiddle generator and fixed/floating converter.


import twiddle_generator as tw

import unittest
import random
class TestTwiddleGeneration(unittest.TestCase):
    def test_real(self):
        self.assertAlmostEqual(1, tw.twiddle(8,0)[0])
        self.assertAlmostEqual(0, tw.twiddle(8,2)[0])
        self.assertAlmostEqual(-1, tw.twiddle(8,4)[0])
        self.assertAlmostEqual(0, tw.twiddle(8,6)[0])
    
    def test_imag(self):
        self.assertAlmostEqual(0, tw.twiddle(8,0)[1])
        self.assertAlmostEqual(-1, tw.twiddle(8,2)[1])
        self.assertAlmostEqual(0, tw.twiddle(8,4)[1])
        self.assertAlmostEqual(1, tw.twiddle(8,6)[1])

    def test_cyclic(self):
        # aim to test the cyclic property of twiddle factors.
        for _ in range(1000):
            base = random.randint(1,128)
            idx = random.randint(1,base)
            normal_result = tw.twiddle(base, idx)
            cycle_result = tw.twiddle(base, base+idx)
            self.assertAlmostEqual(normal_result[0], cycle_result[0])
            self.assertAlmostEqual(normal_result[1], cycle_result[1])


class TestFixedConversion(unittest.TestCase):
    def test_known_positive(self):

        self.assertEqual('0000000101000000', tw.float_to_fixed_binary(1.25,16,8))
        self.assertEqual(1.25, tw.fixed_binary_to_float('0000000101000000',16,8))

    def test_negative(self):
        expected_binstr = '1111111011000000'
        self.assertEqual(expected_binstr, tw.float_to_fixed_binary(-1.25,16,8))
        self.assertEqual(-1.25, tw.fixed_binary_to_float(expected_binstr,16,8))

    def test_random(self):
        for _ in range(1000):
            num = random.uniform(-128,127)

            res = tw.float_to_fixed_binary(num,16,8)
            res = tw.fixed_binary_to_float(res,16,8)

            self.assertAlmostEqual(res, num, delta=0.004) # delta is from q-format calculator
            # exact resolution is 0.00390625 aka 1/(2^8)


