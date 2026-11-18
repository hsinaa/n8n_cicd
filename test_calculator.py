import math

import pytest

import calculator as calc
from calculator import CalculatorError


# ---------- basic ----------
def test_add():
    assert calc.add(2, 3) == 6


def test_subtract():
    assert calc.subtract(5, 7) == -2


def test_multiply():
    assert calc.multiply(4, 2.5) == 10


def test_divide():
    assert calc.divide(9, 3) == 3


def test_divide_by_zero():
    with pytest.raises(CalculatorError):
        calc.divide(1, 0)


def test_modulo():
    assert calc.modulo(10, 3) == 1


# ---------- advanced ----------
def test_power():
    assert calc.power(2, 10) == 1024
    assert calc.power(9, 0.5) == 3


def test_power_negative_base_fractional_exponent():
    with pytest.raises(CalculatorError):
        calc.power(-8, 0.5)


def test_exponential():
    assert calc.exponential(0) == 1
    assert calc.exponential(1) == pytest.approx(math.e)


def test_exponential_overflow():
    with pytest.raises(CalculatorError):
        calc.exponential(10000)


def test_ln():
    assert calc.ln(math.e) == pytest.approx(1)
    assert calc.ln(1) == 0


@pytest.mark.parametrize("bad", [0, -5])
def test_ln_invalid(bad):
    with pytest.raises(CalculatorError):
        calc.ln(bad)


def test_log10():
    assert calc.log10(1000) == pytest.approx(3)


def test_log10_invalid():
    with pytest.raises(CalculatorError):
        calc.log10(0)


def test_log_base():
    assert calc.log_base(8, 2) == pytest.approx(3)


def test_log_base_invalid():
    with pytest.raises(CalculatorError):
        calc.log_base(8, 1)


def test_sqrt():
    assert calc.sqrt(16) == 4
    with pytest.raises(CalculatorError):
        calc.sqrt(-1)


def test_factorial():
    assert calc.factorial(5) == 120
    with pytest.raises(CalculatorError):
        calc.factorial(-1)
    with pytest.raises(CalculatorError):
        calc.factorial(2.5)


# ---------- trig ----------
def test_sin_cos_degrees():
    assert calc.sin(30, degrees=True) == pytest.approx(0.5)
    assert calc.cos(60, degrees=True) == pytest.approx(0.5)


def test_sin_cos_radians():
    assert calc.sin(math.pi / 2) == pytest.approx(1)
    assert calc.cos(math.pi) == pytest.approx(-1)


def test_tan():
    assert calc.tan(45, degrees=True) == pytest.approx(1)


def test_tan_undefined():
    with pytest.raises(CalculatorError):
        calc.tan(90, degrees=True)


# ---------- expression evaluator ----------
def test_evaluate_precedence():
    assert calc.evaluate("2 + 3 * 4") == 14


def test_evaluate_power_symbol():
    assert calc.evaluate("2^3") == 8


def test_evaluate_functions():
    assert calc.evaluate("ln(e)") == pytest.approx(1)
    assert calc.evaluate("log(100)") == pytest.approx(2)
    assert calc.evaluate("exp(0)") == 1
    assert calc.evaluate("sqrt(81)") == 9
    assert calc.evaluate("fact(4)") == 24


def test_evaluate_trig_modes():
    assert calc.evaluate("sin(30)", degrees=True) == pytest.approx(0.5)
    assert calc.evaluate("sin(pi/2)", degrees=False) == pytest.approx(1)


def test_evaluate_unicode_symbols():
    assert calc.evaluate("6÷2×3") == 9
    assert calc.evaluate("√(9)") == 3


def test_evaluate_division_by_zero():
    with pytest.raises(CalculatorError):
        calc.evaluate("5/0")


@pytest.mark.parametrize("bad", ["", "2 +", "foo(3)", "__import__('os')", "2 ** ", "abc"])
def test_evaluate_rejects_bad_input(bad):
    with pytest.raises(CalculatorError):
        calc.evaluate(bad)


# ---------- formatting ----------
def test_format_result():
    assert calc.format_result(8.0) == "8"
    assert calc.format_result(0.1 + 0.2) == "0.3"
    assert calc.format_result(1e-15) == "0"
    assert calc.format_result(math.pi) == "3.141592654"
