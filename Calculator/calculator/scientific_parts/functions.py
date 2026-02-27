"""Public scientific mathematical function wrappers."""

from decimal import Decimal

from calculator.scientific_parts.core import (
    NumberLike,
    _acosh_decimal,
    _acos_decimal,
    _asin_decimal,
    _asinh_decimal,
    _atan_decimal,
    _atanh_decimal,
    _cos_decimal,
    _cosh_decimal,
    _degrees,
    _radians,
    _sin_decimal,
    _sinh_decimal,
    _tanh_decimal,
    _to_decimal,
)


def sine(angle: NumberLike) -> Decimal:
    return _sin_decimal(_radians(_to_decimal(angle)))


def cosine(angle: NumberLike) -> Decimal:
    return _cos_decimal(_radians(_to_decimal(angle)))


def tangent(angle: NumberLike) -> Decimal:
    return _sin_decimal(_radians(_to_decimal(angle))) / _cos_decimal(_radians(_to_decimal(angle)))


def cot(angle: NumberLike) -> Decimal:
    rad = _radians(_to_decimal(angle))
    return _cos_decimal(rad) / _sin_decimal(rad)


def sec(angle: NumberLike) -> Decimal:
    return Decimal(1) / _cos_decimal(_radians(_to_decimal(angle)))


def cosec(angle: NumberLike) -> Decimal:
    return Decimal(1) / _sin_decimal(_radians(_to_decimal(angle)))


def sine_inv(val: NumberLike) -> Decimal:
    return _degrees(_asin_decimal(_to_decimal(val)))


def cosine_inv(val: NumberLike) -> Decimal:
    return _degrees(_acos_decimal(_to_decimal(val)))


def tangent_inv(val: NumberLike) -> Decimal:
    return _degrees(_atan_decimal(_to_decimal(val)))


def cot_inv(val: NumberLike) -> Decimal:
    return _degrees(_atan_decimal(Decimal(1) / _to_decimal(val)))


def sec_inv(val: NumberLike) -> Decimal:
    return _degrees(_acos_decimal(Decimal(1) / _to_decimal(val)))


def cosec_inv(val: NumberLike) -> Decimal:
    return _degrees(_asin_decimal(Decimal(1) / _to_decimal(val)))


def sineh(val: NumberLike) -> Decimal:
    return _sinh_decimal(_to_decimal(val))


def cosineh(val: NumberLike) -> Decimal:
    return _cosh_decimal(_to_decimal(val))


def tangenth(val: NumberLike) -> Decimal:
    return _tanh_decimal(_to_decimal(val))


def coth(val: NumberLike) -> Decimal:
    val_dec = _to_decimal(val)
    return _cosh_decimal(val_dec) / _sinh_decimal(val_dec)


def sech(val: NumberLike) -> Decimal:
    return Decimal(1) / _cosh_decimal(_to_decimal(val))


def cosech(val: NumberLike) -> Decimal:
    return Decimal(1) / _sinh_decimal(_to_decimal(val))


def sineh_inv(val: NumberLike) -> Decimal:
    return _asinh_decimal(_to_decimal(val))


def cosineh_inv(val: NumberLike) -> Decimal:
    return _acosh_decimal(_to_decimal(val))


def tangenth_inv(val: NumberLike) -> Decimal:
    return _atanh_decimal(_to_decimal(val))


def coth_inv(val: NumberLike) -> Decimal:
    val_dec = _to_decimal(val)
    return _atanh_decimal(Decimal(1) / val_dec)


def sech_inv(val: NumberLike) -> Decimal:
    return _acosh_decimal(Decimal(1) / _to_decimal(val))


def cosech_inv(val: NumberLike) -> Decimal:
    return _asinh_decimal(Decimal(1) / _to_decimal(val))
