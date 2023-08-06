#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright © 2019, Matjaž Guštin <dev@matjaz.it> <https://matjaz.it>.
# Released under the BSD 3-Clause License

"""Unit tests of the rangeforce module."""

import unittest

import rangeforce as rf


class TestClip(unittest.TestCase):
    def test_in_range(self):
        self.assertEqual(2, rf.clip(2, 0, 3))
        self.assertEqual(2, rf.clip(2, 1, 3))
        self.assertEqual(2, rf.clip(2, 2, 3))
        self.assertEqual(2, rf.clip(2, 2, 2))
        self.assertEqual(3, rf.clip(3, 2, 3))
        self.assertEqual(3, rf.clip(3, -22, 3))

    def test_negative_in_range(self):
        self.assertEqual(-3, rf.clip(-3, -20, -1))
        self.assertEqual(-3, rf.clip(-3, -5, -1))
        self.assertEqual(-3, rf.clip(-3, -3, -2))
        self.assertEqual(-3, rf.clip(-3, -3, -3))
        self.assertEqual(-3, rf.clip(-3, -3, 1))

    def test_smaller_than_range(self):
        self.assertEqual(10, rf.clip(5, 10, 20))
        self.assertEqual(10, rf.clip(9, 10, 20))
        self.assertEqual(10, rf.clip(0, 10, 20))
        self.assertEqual(10, rf.clip(-10, 10, 20))
        self.assertEqual(-10, rf.clip(-15, -10, 20))

    def test_larger_than_range(self):
        self.assertEqual(20, rf.clip(30, 10, 20))
        self.assertEqual(20, rf.clip(25, 10, 20))
        self.assertEqual(20, rf.clip(21, -10, 20))
        self.assertEqual(-20, rf.clip(-2, -50, -20))
        self.assertEqual(-20, rf.clip(0, -50, -20))
        self.assertEqual(-20, rf.clip(1, -50, -20))


class TestUnsignedInts(unittest.TestCase):
    def test_uint8(self):
        self.assertRaises(rf.RangeError, rf.uint8, -1)
        self.assertRaises(rf.RangeError, rf.uint8, -20)
        self.assertRaises(rf.RangeError, rf.uint8, 2**8)
        self.assertRaises(rf.RangeError, rf.uint8, 300)
        for i in range(0, 2**8):
            self.assertEqual(i, rf.uint8(i))
            self.assertIs(i, rf.uint8(i))

    def test_uint16(self):
        self.assertRaises(rf.RangeError, rf.uint16, -1)
        self.assertRaises(rf.RangeError, rf.uint16, -20)
        self.assertRaises(rf.RangeError, rf.uint16, 2**16)
        self.assertRaises(rf.RangeError, rf.uint16, 5446345)
        for i in range(0, 2**16):
            self.assertEqual(i, rf.uint16(i))
            self.assertIs(i, rf.uint16(i))

    def test_uint32(self):
        self.assertRaises(rf.RangeError, rf.uint32, -1)
        self.assertRaises(rf.RangeError, rf.uint32, -20)
        self.assertRaises(rf.RangeError, rf.uint32, 2**32)
        self.assertRaises(rf.RangeError, rf.uint32, 45874349824936)
        rf.uint32(0)
        rf.uint32(1)
        rf.uint32(2)
        rf.uint32(0xFFFFFFFE)
        rf.uint32(0xFFFFFFFF)
        for i in range(0, 0xFFFFFFFF, 4000):
            self.assertEqual(i, rf.uint32(i))
            self.assertIs(i, rf.uint32(i))

    def test_uint64(self):
        self.assertRaises(rf.RangeError, rf.uint64, -1)
        self.assertRaises(rf.RangeError, rf.uint64, -20)
        self.assertRaises(rf.RangeError, rf.uint64, 2**64)
        self.assertRaises(rf.RangeError, rf.uint64,
                          345837634922573643925763492312573634)
        rf.uint64(0)
        rf.uint64(1)
        rf.uint64(2)
        rf.uint64(2**64 - 2)
        rf.uint64(2**64 - 1)
        for i in range(0, 0xFFFFFFFFFFFFFFFF, 30000000000000):
            self.assertEqual(i, rf.uint64(i))
            self.assertIs(i, rf.uint64(i))

    def test_uint_bits(self):
        self.assertRaises(rf.RangeError, rf.uint_bits, 8, 3)
        self.assertRaises(rf.RangeError, rf.uint_bits, 8, 2)
        self.assertRaises(rf.RangeError, rf.uint_bits, -1, 2)
        self.assertRaises(rf.RangeError, rf.uint_bits, -8, 2)
        for i in range(0, 8):
            self.assertEqual(i, rf.uint_bits(i, 3))
            self.assertIs(i, rf.uint_bits(i, 3))
        for i in range(0, 16):
            self.assertEqual(i, rf.uint_bits(i, 4))
            self.assertIs(i, rf.uint_bits(i, 4))


class TestSignedInts(unittest.TestCase):
    def test_int8(self):
        self.assertRaises(rf.RangeError, rf.int8, -2**7 - 1)
        self.assertRaises(rf.RangeError, rf.int8, -150)
        self.assertRaises(rf.RangeError, rf.int8, 2**7)
        self.assertRaises(rf.RangeError, rf.int8, 1560)
        for i in range(-128, 127):
            self.assertEqual(i, rf.int8(i))
            self.assertIs(i, rf.int8(i))

    def test_int16(self):
        self.assertRaises(rf.RangeError, rf.int16, -2**15 - 1)
        self.assertRaises(rf.RangeError, rf.int16, -675832495)
        self.assertRaises(rf.RangeError, rf.int16, 2**15)
        self.assertRaises(rf.RangeError, rf.int16, 5446345)
        for i in range(-32768, 32767):
            self.assertEqual(i, rf.int16(i))
            self.assertIs(i, rf.int16(i))

    def test_int32(self):
        self.assertRaises(rf.RangeError, rf.int32, -2**31 - 1)
        self.assertRaises(rf.RangeError, rf.int32, 2**31)
        self.assertRaises(rf.RangeError, rf.int32, 45874349824936)
        rf.int32(-0x8000000)
        rf.int32(-0x8000000 + 1)
        rf.int32(-2)
        rf.int32(-1)
        rf.int32(0)
        rf.int32(1)
        rf.int32(2)
        rf.int32(0x7FFFFFFE)
        rf.int32(0x7FFFFFFF)
        for i in range(-0x8000000, 0x7FFFFFFF, 4000):
            self.assertEqual(i, rf.int32(i))
            self.assertIs(i, rf.int32(i))

    def test_int64(self):
        self.assertRaises(rf.RangeError, rf.int64, -2**64 - 1)
        self.assertRaises(rf.RangeError, rf.int64, 2**64)
        self.assertRaises(rf.RangeError, rf.int64,
                          345837634922573643925763492312573634)
        rf.int64(-0x8000000000000000)
        rf.int64(-0x8000000000000000 + 1)
        rf.int64(-2)
        rf.int64(-1)
        rf.int64(0)
        rf.int64(1)
        rf.int64(2)
        rf.int64(0x7FFFFFFFFFFFFFFE)
        rf.int64(0x7FFFFFFFFFFFFFFF)
        for i in range(-0x8000000000000000, 0x7FFFFFFFFFFFFFFF,
                       30000000000000):
            self.assertEqual(i, rf.int64(i))
            self.assertIs(i, rf.int64(i))


class TestNegativePositiveInt(unittest.TestCase):
    def test_negative_int(self):
        self.assertRaises(rf.RangeError, rf.negative_int, 0)
        self.assertRaises(rf.RangeError, rf.negative_int, 1)
        self.assertRaises(rf.RangeError, rf.negative_int, 100)
        self.assertEqual(-20, rf.negative_int(-20))
        self.assertIs(-20, rf.negative_int(-20))

    def test_nonpositive_int(self):
        self.assertRaises(rf.RangeError, rf.nonpositive_int, 1)
        self.assertRaises(rf.RangeError, rf.nonpositive_int, 100)
        self.assertEqual(-20, rf.nonpositive_int(-20))
        self.assertIs(-20, rf.nonpositive_int(-20))
        self.assertEqual(0, rf.nonpositive_int(0))
        self.assertIs(0, rf.nonpositive_int(0))

    def test_positive_int(self):
        self.assertRaises(rf.RangeError, rf.positive_int, 0)
        self.assertRaises(rf.RangeError, rf.positive_int, -1)
        self.assertRaises(rf.RangeError, rf.positive_int, -100)
        self.assertEqual(20, rf.positive_int(20))
        self.assertIs(20, rf.positive_int(20))

    def test_nonnegative_int(self):
        self.assertRaises(rf.RangeError, rf.nonnegative_int, -1)
        self.assertRaises(rf.RangeError, rf.nonnegative_int, -100)
        self.assertEqual(20, rf.nonnegative_int(20))
        self.assertIs(20, rf.nonnegative_int(20))
        self.assertEqual(0, rf.nonnegative_int(0))
        self.assertIs(0, rf.nonnegative_int(0))


class TestLimited(unittest.TestCase):
    def test_in_closed_range(self):
        for i in range(100):
            self.assertEqual(i, rf.limited(i, 0, 99))
        for i in range(100):
            self.assertEqual(i + 0.1, rf.limited(i + 0.1, 0, 100))

    def test_in_open_range_upper_bound(self):
        for i in range(100):
            self.assertEqual(i, rf.limited(i, 0, None))
        for i in range(100):
            self.assertEqual(i + 0.1, rf.limited(i + 0.1, 0, None))

    def test_in_open_range_on_lower_bound(self):
        for i in range(100):
            self.assertEqual(i, rf.limited(i, None, 99))
        for i in range(100):
            self.assertEqual(i + 0.1, rf.limited(i + 0.1, None, 99.2))

    def test_below_closed_range(self):
        expected_message = 'Value must be in range [100, 1000]. ' \
                           '2 found instead.'
        with self.assertRaises(rf.RangeError) as ex:
            rf.limited(2, 100, 1000)
        self.assertEqual(expected_message, str(ex.exception))

    def test_below_open_range_on_upper_bound(self):
        expected_message = 'Value must be in range [100, +inf[. ' \
                           '2 found instead.'
        with self.assertRaises(rf.RangeError) as ex:
            rf.limited(2, 100, None)
        self.assertEqual(expected_message, str(ex.exception))

    def test_above_closed_range(self):
        expected_message = 'Value must be in range [100, 1000]. ' \
                           '2000 found instead.'
        with self.assertRaises(rf.RangeError) as ex:
            rf.limited(2000, 100, 1000)
        self.assertEqual(expected_message, str(ex.exception))

    def test_above_open_range_on_lower_bound(self):
        expected_message = 'Value must be in range ]-inf, 1000]. ' \
                           '2000 found instead.'
        with self.assertRaises(rf.RangeError) as ex:
            rf.limited(2000, None, 1000)
        self.assertEqual(expected_message, str(ex.exception))

    def test_custom_value_name(self):
        expected_message = 'HELLO must be in range [100, 1000]. ' \
                           '2 found instead.'
        with self.assertRaises(rf.RangeError) as ex:
            rf.limited(2, 100, 1000, 'HELLO')
        self.assertEqual(expected_message, str(ex.exception))
        expected_message = 'HELLO must be in range [100, +inf[. ' \
                           '2 found instead.'
        with self.assertRaises(rf.RangeError) as ex:
            rf.limited(2, 100, None, 'HELLO')
        self.assertEqual(expected_message, str(ex.exception))
        expected_message = 'HELLO must be in range [100, 1000]. ' \
                           '2000 found instead.'
        with self.assertRaises(rf.RangeError) as ex:
            rf.limited(2000, 100, 1000, 'HELLO')
        self.assertEqual(expected_message, str(ex.exception))
        expected_message = 'HELLO must be in range ]-inf, 1000]. ' \
                           '2000 found instead.'
        with self.assertRaises(rf.RangeError) as ex:
            rf.limited(2000, None, 1000, 'HELLO')
        self.assertEqual(expected_message, str(ex.exception))

    def test_plus_infinity(self):
        inf = float('+inf')
        expected_message = 'Value must be in range [0.0, 1.0]. ' \
                           'inf found instead.'
        with self.assertRaises(rf.RangeError) as ex:
            rf.limited(inf, 0.0, 1.0)
        self.assertEqual(expected_message, str(ex.exception))
        expected_message = 'Value must be in range ]-inf, 1.0]. ' \
                           'inf found instead.'
        with self.assertRaises(rf.RangeError) as ex:
            rf.limited(inf, None, 1.0)
        self.assertEqual(expected_message, str(ex.exception))
        self.assertEqual(inf, rf.limited(inf, 0, None))

    def test_minus_infinity(self):
        minf = float('-inf')
        expected_message = 'Value must be in range [0.0, 1.0]. ' \
                           '-inf found instead.'
        with self.assertRaises(rf.RangeError) as ex:
            rf.limited(minf, 0.0, 1.0)
        self.assertEqual(expected_message, str(ex.exception))
        expected_message = 'Value must be in range [0.0, +inf[. ' \
                           '-inf found instead.'
        with self.assertRaises(rf.RangeError) as ex:
            rf.limited(minf, 0.0, None)
        self.assertEqual(expected_message, str(ex.exception))
        self.assertEqual(minf, rf.limited(minf, None, 0))

    def test_nan(self):
        nan = float('nan')
        expected_message = 'Value must be in range [0.0, 1.0]. ' \
                           'nan found instead.'
        with self.assertRaises(rf.RangeError) as ex:
            rf.limited(nan, 0.0, 1.0)
        self.assertEqual(expected_message, str(ex.exception))
        expected_message = 'Value must be in range [0.0, +inf[. ' \
                           'nan found instead.'
        with self.assertRaises(rf.RangeError) as ex:
            rf.limited(nan, 0.0, None)
        self.assertEqual(expected_message, str(ex.exception))
        expected_message = 'Value must be in range ]-inf, 0]. ' \
                           'nan found instead.'
        with self.assertRaises(rf.RangeError) as ex:
            rf.limited(nan, None, 0)
        self.assertEqual(expected_message, str(ex.exception))

    def test_infinity_instead_of_none(self):
        self.assertEqual(10, rf.limited(10, float('-inf'), 20))

    def test_double_none(self):
        expected_message = '[min, max] interval must be closed on at least ' \
                           'one extreme.'
        with self.assertRaises(ValueError) as ex:
            rf.limited(10, None, None)
        self.assertEqual(expected_message, str(ex.exception))

    def test_unsorted_bounds(self):
        expected_message = 'Interval extremes [20, 15] not in order.'
        with self.assertRaises(ValueError) as ex:
            rf.limited(10, 20, 15)
        self.assertEqual(expected_message, str(ex.exception))

    def test_nan_interval_extreme(self):
        expected_message = 'NaN is not a valid interval upper bound.'
        with self.assertRaises(ValueError) as ex:
            rf.limited(10, 5, float('nan'))
        self.assertEqual(expected_message, str(ex.exception))
        expected_message = 'NaN is not a valid interval lower bound.'
        with self.assertRaises(ValueError) as ex:
            rf.limited(10, float('nan'), 5)
        self.assertEqual(expected_message, str(ex.exception))

    def test_enforce_type(self):
        self.assertEqual(2, rf.limited(2, 0, 10, dtype=int))
        expected_message = 'Value must be of type int. float found instead.'
        with self.assertRaises(TypeError) as ex:
            rf.limited(2.0, 0, 10, dtype=int)
        self.assertEqual(expected_message, str(ex.exception))


class TestLimitedLen(unittest.TestCase):
    def test_in_closed_range(self):
        for i in range(100):
            self.assertEqual([2] * i, rf.limited_len([2] * i, 0, 99))

    def test_in_open_range_upper_bound(self):
        for i in range(100):
            self.assertEqual([2] * i, rf.limited_len([2] * i, 0, None))

    def test_in_open_range_on_lower_bound(self):
        for i in range(100):
            self.assertEqual([2] * i, rf.limited_len([2] * i, None, 99))

    def test_below_closed_range(self):
        expected_message = 'Length of value must be in range [100, 1000]. ' \
                           '2 found instead.'
        with self.assertRaises(rf.RangeError) as ex:
            rf.limited_len([2] * 2, 100, 1000)
        self.assertEqual(expected_message, str(ex.exception))

    def test_below_open_range_on_upper_bound(self):
        expected_message = 'Length of value must be in range [100, +inf[. ' \
                           '2 found instead.'
        with self.assertRaises(rf.RangeError) as ex:
            rf.limited_len([2] * 2, 100, None)
        self.assertEqual(expected_message, str(ex.exception))

    def test_above_closed_range(self):
        expected_message = 'Length of value must be in range [100, 1000]. ' \
                           '2000 found instead.'
        with self.assertRaises(rf.RangeError) as ex:
            rf.limited_len([2] * 2000, 100, 1000)
        self.assertEqual(expected_message, str(ex.exception))

    def test_above_open_range_on_lower_bound(self):
        expected_message = 'Length of value must be in range ]-inf, 1000]. ' \
                           '2000 found instead.'
        with self.assertRaises(rf.RangeError) as ex:
            rf.limited_len([2] * 2000, None, 1000)
        self.assertEqual(expected_message, str(ex.exception))

    def test_custom_value_name(self):
        expected_message = 'Length of HELLO must be in range [100, 1000]. ' \
                           '2 found instead.'
        with self.assertRaises(rf.RangeError) as ex:
            rf.limited_len([2] * 2, 100, 1000, 'HELLO')
        self.assertEqual(expected_message, str(ex.exception))
        expected_message = 'Length of HELLO must be in range [100, +inf[. ' \
                           '2 found instead.'
        with self.assertRaises(rf.RangeError) as ex:
            rf.limited_len([2] * 2, 100, None, 'HELLO')
        self.assertEqual(expected_message, str(ex.exception))
        expected_message = 'Length of HELLO must be in range [100, 1000]. ' \
                           '2000 found instead.'
        with self.assertRaises(rf.RangeError) as ex:
            rf.limited_len([2] * 2000, 100, 1000, 'HELLO')
        self.assertEqual(expected_message, str(ex.exception))
        expected_message = 'Length of HELLO must be in range ]-inf, 1000]. ' \
                           '2000 found instead.'
        with self.assertRaises(rf.RangeError) as ex:
            rf.limited_len([2] * 2000, None, 1000, 'HELLO')
        self.assertEqual(expected_message, str(ex.exception))

    def test_negative_min_length(self):
        expected_message = 'Length lower bound must be non-negative. ' \
                           '-2 found instead.'
        with self.assertRaises(ValueError) as ex:
            rf.limited_len([2] * 2, -2, 10)
        self.assertEqual(expected_message, str(ex.exception))

    def test_negative_max_length(self):
        expected_message = 'Length upper bound must be non-negative. ' \
                           '-3 found instead.'
        with self.assertRaises(ValueError) as ex:
            rf.limited_len([2] * 2, 0.0, -3)
        self.assertEqual(expected_message, str(ex.exception))

    def test_infinity_instead_of_none(self):
        self.assertEqual([2] * 10, rf.limited_len([2] * 10, 2, float('+inf')))

    def test_double_none(self):
        expected_message = '[min, max] interval must be closed on at least ' \
                           'one extreme.'
        with self.assertRaises(ValueError) as ex:
            rf.limited_len([2] * 10, None, None)
        self.assertEqual(expected_message, str(ex.exception))

    def test_unsorted_bounds(self):
        expected_message = 'Interval extremes [20, 15] not in order.'
        with self.assertRaises(ValueError) as ex:
            rf.limited_len([2] * 10, 20, 15)
        self.assertEqual(expected_message, str(ex.exception))

    def test_nan_interval_extreme(self):
        expected_message = 'NaN is not a valid interval upper bound.'
        with self.assertRaises(ValueError) as ex:
            rf.limited_len([2] * 10, 5, float('nan'))
        self.assertEqual(expected_message, str(ex.exception))
        expected_message = 'NaN is not a valid interval lower bound.'
        with self.assertRaises(ValueError) as ex:
            rf.limited_len([2] * 10, float('nan'), 5)
        self.assertEqual(expected_message, str(ex.exception))


class TestExactLen(unittest.TestCase):
    def test_proper_length(self):
        self.assertEqual([2] * 2, rf.exact_len([2] * 2, 2))

    def test_zero_length(self):
        self.assertEqual([], rf.exact_len([], 0))

    def test_smaller_length(self):
        expected_message = 'Length of value must be exactly 3. ' \
                           '2 found instead.'
        with self.assertRaises(rf.RangeError) as ex:
            rf.exact_len([2] * 2, 3)
        self.assertEqual(expected_message, str(ex.exception))

    def test_greater_length(self):
        expected_message = 'Length of value must be exactly 3. ' \
                           '5 found instead.'
        with self.assertRaises(rf.RangeError) as ex:
            rf.exact_len([2] * 5, 3)
        self.assertEqual(expected_message, str(ex.exception))

    def test_custom_value_name(self):
        expected_message = 'Length of HELLO must be exactly 1. ' \
                           '2 found instead.'
        with self.assertRaises(rf.RangeError) as ex:
            rf.exact_len([2] * 2, 1, 'HELLO')
        self.assertEqual(expected_message, str(ex.exception))
        expected_message = 'Length of HELLO WORLD must be exactly 5. ' \
                           '2 found instead.'
        with self.assertRaises(rf.RangeError) as ex:
            rf.exact_len([2] * 2, 5, 'HELLO WORLD')
        self.assertEqual(expected_message, str(ex.exception))

    def test_negative_expected_length(self):
        expected_message = 'Expected length must be non-negative. ' \
                           '-2 found instead.'
        with self.assertRaises(ValueError) as ex:
            rf.exact_len([2] * 2, -2)
        self.assertEqual(expected_message, str(ex.exception))

    def test_expected_length_must_be_int(self):
        expected_message = 'Expected length must be an integer. ' \
                           'NoneType found instead.'
        with self.assertRaises(TypeError) as ex:
            rf.exact_len([2] * 2, None)
        self.assertEqual(expected_message, str(ex.exception))
        expected_message = 'Expected length must be an integer. ' \
                           'float found instead.'
        with self.assertRaises(TypeError) as ex:
            rf.exact_len([2] * 2, 2.0)
        self.assertEqual(expected_message, str(ex.exception))
        expected_message = 'Expected length must be an integer. ' \
                           'float found instead.'
        with self.assertRaises(TypeError) as ex:
            rf.exact_len([2] * 2, float('+inf'))
        self.assertEqual(expected_message, str(ex.exception))
        expected_message = 'Expected length must be an integer. ' \
                           'float found instead.'
        with self.assertRaises(TypeError) as ex:
            rf.exact_len([2] * 2, float('nan'))
        self.assertEqual(expected_message, str(ex.exception))
