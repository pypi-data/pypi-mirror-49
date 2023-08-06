#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright © 2019, Matjaž Guštin <dev@matjaz.it> <https://matjaz.it>.
# Released under the BSD 3-Clause License

"""Rangeforce, a developer-friendly check for "is this value
within the allowed range?" with user-friendly error messages.

Rangeforce aims to simplify the input validation process  where the error
message of the exception is shown directly to the user and has to be
understandable, which may happened in a command line interface or when using
a Python program interactively from a Python shell.

For example:

        value = int(input('How many hours per day do you sleep? '))
        value = rangeforce.limited(value, 0, 24, name='Hours of sleep')
        # Now value is valid. Otherwise an error message like this appears:
        # rangeforce.RangeError: Hours of sleep must be in range [0, 24]. 25 found instead.

        # Expecially useful for values that need to fit within an integer type:
        value = rangeforce.uint16(int(input('Type a 16-bit value: ')))
        rangeforce.RangeError: Value must be in range [0, 65535]. 70000 found instead.
"""

import math

__VERSION__ = '1.0.0'


class RangeError(Exception):
    """Value outside of the allowed range.

    A custom exception type raised by Rangeforce functions when the validation
    of the values fails, that is when the values are not within the acceptable
    bounds.
    """
    pass


def clip(value, min, max):
    """Clips (limits) the value to the given limits.

    The output is at least `min`, at most `max` and `value` if that value
    is between the `min` and `max`.

    Args:
        value: to be limited to [min, max]
        min: smallest acceptable value
        max: greatest acceptable value

    Returns:
        the given value if within [min, max] or min if value is smaller than
        min or max if value is greater than max.
    """
    if value < min:
        return min
    elif value > max:
        return max
    else:
        return value


def limited(value, min, max, name='Value', dtype=None):
    """Validates that value is within the [min, max] interval.

    If the value is valid, it returns the value itself.
    If the value is not valid, it raises a RangeError with an understandable
    error message that includes expected range and failing value.

    Either min or max can be set to None for an unbound validity interval, i.e.
    the value only has to be smaller or greater than something, not within a
    closed interval.

    The name of the value can be altered for a customized error message.

    The data type can be enforced if specified.

    Args:
        value: the value to be validated to be within [min, max]
        min: smallest acceptable value. Can be None if max is not None.
             Can be +inf, -inf. Cannot be NaN. Must be <= max.
        max: greatest acceptable value. Can be None if min is not None.
             Can be +inf, -inf. Cannot be NaN. Must be >= min.
        name: customizable name of the value that appears in the error message
        dtype: optional data type the value has to be

    Returns:
        the given value if within [min, max] and, optionally, of the correct
        data type

    Raises:
        RangeError: if the value is not within the acceptable range.
        TypeError: if the value is not of the acceptable data type, if
                   specified.
        ValueError: if the min, max extremes are not valid (e.g. both None,
                    min greater than max, NaN etc.)

    Examples:
            >>> limited(0.5, 0, 1)  # Valid value
            0.5
            >>> limited(500, 0.1, 42)  # Value out of range
            rangeforce.RangeError: Value must be in range [0.1, -42]. 500
            found instead.
            >>> limited(50, 0, 24, name='Hours in a day')
            rangeforce.RangeError: Hours in a day must be in range [0,
            24]. 50 found instead.
            >>> limited(-1, 0, None, name='Earth satellites')
            rangeforce.RangeError: Earth satellites must be in range [0,
            +inf[. -1 found instead.
            >>> limited(1.1, 0, None, name='Earth satellites', dtype=int)
            TypeError: Earth satellites must be of type int. float found
            instead.
    """
    _validate_interval(min, max)
    _validate_type(name, value, dtype)
    if min is None and max is not None and (value > max or math.isnan(value)):
        raise RangeError(
            '{:} must be in range ]-inf, {:}]. '
            '{:} found instead.'.format(name, max, value)
        )
    elif max is None and min is not None and (
            value < min or math.isnan(value)):
        raise RangeError(
            '{:} must be in range [{:}, +inf[. '
            '{:} found instead.'.format(name, min, value)
        )
    elif min is not None and max is not None and (
            value < min or value > max or math.isnan(value)):
        raise RangeError(
            '{:} must be in range [{:}, {:}]. '
            '{:} found instead.'.format(name, min, max, value)
        )
    else:
        return value


def _validate_interval(min, max):
    if min is None and max is None:
        raise ValueError(
            '[min, max] interval must be closed on at least one extreme.')
    elif min is not None and math.isnan(min):
        raise ValueError('NaN is not a valid interval lower bound.')
    elif max is not None and math.isnan(max):
        raise ValueError('NaN is not a valid interval upper bound.')
    elif min is not None and max is not None and min > max:
        raise ValueError(
            'Interval extremes [{:}, {:}] not in order.'.format(min, max))


def _validate_type(name, value, dtype):
    if dtype is not None and not isinstance(value, dtype):
        raise TypeError(
            '{:} must be of type {:}. '
            '{:} found instead.'.format(name, dtype.__name__,
                                        type(value).__name__)
        )


def negative_int(value, name='Value'):
    """Validates that value is negative (< 0) and of type int.

    If the value is valid, it returns the value itself.
    If the value is not valid, it raises a RangeError with an understandable
    error message that includes expected range and failing value.

    Args:
        value: the value to be validated to be within ]-inf, 0[
        name: customizable name of the value that appears in the error message

    Returns:
        the given value if < 0

    Raises:
        RangeError: if the value is not within the acceptable range.
        TypeError: if the value is not an integer.
    """
    return limited(value, None, -1, name, dtype=int)


def nonpositive_int(value, name='Value'):
    """Validates that value is non-positive (<= 0) and of type int.

    If the value is valid, it returns the value itself.
    If the value is not valid, it raises a RangeError with an understandable
    error message that includes expected range and failing value.

    Args:
        value: the value to be validated to be within ]-inf, 0]
        name: customizable name of the value that appears in the error message

    Returns:
        the given value if <= 0

    Raises:
        RangeError: if the value is not within the acceptable range.
        TypeError: if the value is not an integer.
    """
    return limited(value, None, 0, name, dtype=int)


def positive_int(value, name='Value'):
    """Validates that value is positive (> 0) and of type int.

    If the value is valid, it returns the value itself.
    If the value is not valid, it raises a RangeError with an understandable
    error message that includes expected range and failing value.

    Args:
        value: the value to be validated to be within ]0, +inf[
        name: customizable name of the value that appears in the error message

    Returns:
        the given value if > 0

    Raises:
        RangeError: if the value is not within the acceptable range.
        TypeError: if the value is not an integer.
    """
    return limited(value, 1, None, name, dtype=int)


def nonnegative_int(value, name='Value'):
    """Validates that value is non-negative (>= 0) and of type int.

    If the value is valid, it returns the value itself.
    If the value is not valid, it raises a RangeError with an understandable
    error message that includes expected range and failing value.

    Args:
        value: the value to be validated to be within [0, +inf[
        name: customizable name of the value that appears in the error message

    Returns:
        the given value if >= 0

    Raises:
        RangeError: if the value is not within the acceptable range.
        TypeError: if the value is not an integer.
    """
    return limited(value, 0, None, name, dtype=int)


def uint8(value, name='Value'):
    """Validates that value fits in an 8-bit unsigned integer.

    If the value is valid, it returns the value itself.
    If the value is not valid, it raises a RangeError with an understandable
    error message that includes expected range and failing value.

    Args:
        value: the value to be validated to be within [0, 255]
        name: customizable name of the value that appears in the error message

    Returns:
        the given value can be expressed in 8 bits (unsigned)

    Raises:
        RangeError: if the value is not within the acceptable range.
        TypeError: if the value is not an integer.
    """
    return limited(value, 0, 0xFF, name, dtype=int)


def uint16(value, name='Value'):
    """Validates that value fits in a 16-bit unsigned integer.

    If the value is valid, it returns the value itself.
    If the value is not valid, it raises a RangeError with an understandable
    error message that includes expected range and failing value.

    Args:
        value: the value to be validated to be within [0, 65535]
        name: customizable name of the value that appears in the error message

    Returns:
        the given value can be expressed in 16 bits (unsigned)

    Raises:
        RangeError: if the value is not within the acceptable range.
        TypeError: if the value is not an integer.
    """
    return limited(value, 0, 0xFFFF, name, dtype=int)


def uint32(value, name='Value'):
    """Validates that value fits in a 32-bit unsigned integer.

    If the value is valid, it returns the value itself.
    If the value is not valid, it raises a RangeError with an understandable
    error message that includes expected range and failing value.

    Args:
        value: the value to be validated to be within [0, 4294967295]
        name: customizable name of the value that appears in the error message

    Returns:
        the given value can be expressed in 32 bits (unsigned)

    Raises:
        RangeError: if the value is not within the acceptable range.
        TypeError: if the value is not an integer.
    """
    return limited(value, 0, 0xFFFFFFFF, name, dtype=int)


def uint64(value, name='Value'):
    """Validates that value fits in a 64-bit unsigned integer.

    If the value is valid, it returns the value itself.
    If the value is not valid, it raises a RangeError with an understandable
    error message that includes expected range and failing value.

    Args:
        value: the value to be validated to be within [0, 18446744073709551615]
        name: customizable name of the value that appears in the error message

    Returns:
        the given value can be expressed in 64 bits (unsigned)

    Raises:
        RangeError: if the value is not within the acceptable range.
        TypeError: if the value is not an integer.
    """
    return limited(value, 0, 0xFFFFFFFFFFFFFFFF, name, dtype=int)


def uint_bits(value, bits, name='Value'):
    """Validates that value fits in an unsigned integer of specified bitlength.

    If the value is valid, it returns the value itself.
    If the value is not valid, it raises a RangeError with an understandable
    error message that includes expected range and failing value.

    Args:
        value: the value to be validated to be within [0, 2**bits-1]
        name: customizable name of the value that appears in the error message

    Returns:
        the given value can be expressed in the given amount of  bits
        (unsigned)

    Raises:
        RangeError: if the value is not within the acceptable range.
        TypeError: if the value is not an integer.
    """
    return limited(value, 0, (1 << bits) - 1, name, dtype=int)


def int8(value, name='Value'):
    """Validates that value fits in an 8-bit signed integer.

    If the value is valid, it returns the value itself.
    If the value is not valid, it raises a RangeError with an understandable
    error message that includes expected range and failing value.

    Args:
        value: the value to be validated to be within [-128, 127]
        name: customizable name of the value that appears in the error message

    Returns:
        the given value can be expressed in 8 bits (signed)

    Raises:
        RangeError: if the value is not within the acceptable range.
        TypeError: if the value is not an integer.
    """
    return limited(value, -0x80, 0x7F, name, dtype=int)


def int16(value, name='Value'):
    """Validates that value fits in a 16-bit signed integer.

    If the value is valid, it returns the value itself.
    If the value is not valid, it raises a RangeError with an understandable
    error message that includes expected range and failing value.

    Args:
        value: the value to be validated to be within [-32768, 32767]
        name: customizable name of the value that appears in the error message

    Returns:
        the given value can be expressed in 16 bits (signed)

    Raises:
        RangeError: if the value is not within the acceptable range.
        TypeError: if the value is not an integer.
    """
    return limited(value, -0x8000, 0x7FFF, name, dtype=int)


def int32(value, name='Value'):
    """Validates that value fits in a 32-bit signed integer.

    If the value is valid, it returns the value itself.
    If the value is not valid, it raises a RangeError with an understandable
    error message that includes expected range and failing value.

    Args:
        value: the value to be validated to be within [-2147483648, 2147483647]
        name: customizable name of the value that appears in the error message

    Returns:
        the given value can be expressed in 32 bits (signed)

    Raises:
        RangeError: if the value is not within the acceptable range.
        TypeError: if the value is not an integer.
    """
    return limited(value, -0x80000000, 0x7FFFFFFF, name, dtype=int)


def int64(value, name='Value'):
    """Validates that value fits in a 16-bit signed integer.

    If the value is valid, it returns the value itself.
    If the value is not valid, it raises a RangeError with an understandable
    error message that includes expected range and failing value.

    Args:
        value: the value to be validated to be within [-9223372036854775808,
               9223372036854775807]
        name: customizable name of the value that appears in the error message

    Returns:
        the given value can be expressed in 64 bits (signed)

    Raises:
        RangeError: if the value is not within the acceptable range.
        TypeError: if the value is not an integer.
    """
    return limited(value, -0x8000000000000000, 0x7FFFFFFFFFFFFFFF, name,
                   dtype=int)


def limited_len(sized, min, max, name='value'):
    """Validates that value has a length within the [min, max] interval.

    If the sized value is valid, it returns the value itself.
    If the sized value is not valid, it raises a RangeError with an
    understandable error message that includes expected length range and
    failing sized value.

    Either min or max can be set to None for an unbound validity
    interval, i.e. the value only has to have a length smaller or greater than
    something, not within a closed interval.

    The name of the sized value can be altered for a customized error message.

    Args:
        sized: the value whose length is to be validated to be within
               [min, max]
        min: smallest acceptable length. Can be None if max is not None.
             Can be +inf, -inf. Cannot be NaN. Must be <= max and >= 0.
        max: greatest acceptable length. Can be None if min is not None.
             Can be +inf, -inf. Cannot be NaN. Must be >= min and >= 0.
        name: customizable name of the value that appears in the error message

    Returns:
        the given sized value if has length within [min, max]

    Raises:
        RangeError: if the value does not have a length within the acceptable
                    range.
        ValueError: if the min, max extremes are not valid (e.g. negative,
                    both None, min greater than max, NaN etc.)

    Examples:
            >>> limited_len([1, 2, 3], 0, 10)  # Valid value
            [1, 2, 3]
            >>> limited_len([1, 2, 3], 0, 2)  # Value out of range
            rangeforce.RangeError: Length of value must be in range [0,
            2]. 3 found instead.
            >>> limited_len([1, 2, 3, 4], 0, 3, name='groups')
            rangeforce.RangeError: Length of groups must be in range [0,
            3]. 4 found instead.
            >>> limited_len([1, 2, 3], 10, None)
            rangeforce.RangeError: Length of value must be in range [10,
            +inf[. 3 found instead.
    """
    length = len(sized)
    _validate_non_negative_interval_extremes(min, max)
    limited(length, min, max, name='Length of ' + name)
    return sized


def _validate_non_negative_interval_extremes(min, max):
    if min is not None and min < 0:
        raise ValueError(
            'Length lower bound must be non-negative. '
            '{:} found instead.'.format(min)
        )
    elif max is not None and max < 0:
        raise ValueError(
            'Length upper bound must be non-negative. '
            '{:} found instead.'.format(max)
        )


def exact_len(sized, expected, name='value'):
    """Validates that value has an exact length.

    If the sized value is valid, it returns the value itself.
    If the sized value is not valid, it raises a RangeError with an
    understandable error message that includes expected length and
    failing sized value.

    The name of the sized value can be altered for a customized error message.

    Args:
        sized: the value whose length is to be validated to be exactly as
               expected.
        expected: only acceptable length. Must be an integer >= 0.
        name: customizable name of the value that appears in the error message

    Returns:
        the given sized value if has length matching the expected

    Raises:
        RangeError: if the value does not have a length matching the expected.
        ValueError: if the expected length is not valid (e.g. not integer,
                    negative, None)

    Examples:
            >>> exact_len([1, 2, 3], 3)  # Valid value
            [1, 2, 3]
            >>> exact_len([1, 2, 3], 2)
            rangeforce.RangeError: Length of value must be exactly 2. 3
            found instead.
            >>> exact_len([1], 2, name='pairs')
            rangeforce.RangeError: Length of pairs must be exactly 2. 1
            found instead.
    """
    length = len(sized)
    _validate_expected_length(expected)
    if length != expected:
        raise RangeError(
            'Length of {:} must be exactly {:}. '
            '{:} found instead.'.format(name, expected, length)
        )
    return sized


def _validate_expected_length(expected):
    if not isinstance(expected, int):
        raise TypeError(
            'Expected length must be an integer. '
            '{:} found instead.'.format(type(expected).__name__)
        )
    elif expected < 0:
        raise ValueError(
            'Expected length must be non-negative. '
            '{:} found instead.'.format(expected)
        )
