"""Calculator logic (no GUI here, so it is easy to test in CI)."""
import ast
import math
import operator


class CalculatorError(ValueError):
    """Raised for any invalid calculation (divide by zero, bad domain...)."""


# ---------- basic operations ----------
def add(a, b):
    return a + b


def subtract(a, b):
    return a - b


def multiply(a, b):
    return a * b


def divide(a, b):
    if b == 0:
        raise CalculatorError("Division by zero")
    return a / b


def modulo(a, b):
    if b == 0:
        raise CalculatorError("Modulo by zero")
    return a % b


# ---------- advanced operations ----------
def power(x, y):
    """x^y"""
    try:
        return math.pow(x, y)
    except OverflowError:
        raise CalculatorError("Result too large")
    except ValueError:
        raise CalculatorError("Invalid power operation")


def exponential(x):
    """e^x"""
    try:
        return math.exp(x)
    except OverflowError:
        raise CalculatorError("Result too large")


def ln(x):
    if x <= 0:
        raise CalculatorError("ln is only defined for x > 0")
    return math.log(x)


def log10(x):
    if x <= 0:
        raise CalculatorError("log is only defined for x > 0")
    return math.log10(x)


def log_base(x, base):
    if x <= 0 or base <= 0 or base == 1:
        raise CalculatorError("Invalid logarithm arguments")
    return math.log(x) / math.log(base)


def sqrt(x):
    if x < 0:
        raise CalculatorError("Square root of a negative number")
    return math.sqrt(x)


def factorial(n):
    if n < 0 or int(n) != n:
        raise CalculatorError("Factorial needs a non-negative integer")
    if n > 170:
        raise CalculatorError("Result too large")
    return float(math.factorial(int(n)))


# ---------- trigonometry (degrees or radians) ----------
def _to_rad(x, degrees):
    return math.radians(x) if degrees else x


def sin(x, degrees=False):
    return math.sin(_to_rad(x, degrees))


def cos(x, degrees=False):
    return math.cos(_to_rad(x, degrees))


def tan(x, degrees=False):
    rad = _to_rad(x, degrees)
    if abs(math.cos(rad)) < 1e-12:
        raise CalculatorError("tan is undefined for this angle")
    return math.tan(rad)


# ---------- safe expression evaluator ----------
_BIN_OPS = {
    ast.Add: add,
    ast.Sub: subtract,
    ast.Mult: multiply,
    ast.Div: divide,
    ast.Mod: modulo,
    ast.Pow: power,
}
_UNARY_OPS = {ast.UAdd: operator.pos, ast.USub: operator.neg}
_CONSTANTS = {"pi": math.pi, "e": math.e}


def _functions(degrees):
    return {
        "sin": lambda x: sin(x, degrees),
        "cos": lambda x: cos(x, degrees),
        "tan": lambda x: tan(x, degrees),
        "ln": ln,
        "log": log10,
        "exp": exponential,
        "sqrt": sqrt,
        "fact": factorial,
        "abs": abs,
    }


def _eval(node, funcs):
    if isinstance(node, ast.Expression):
        return _eval(node.body, funcs)
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    if isinstance(node, ast.Name) and node.id in _CONSTANTS:
        return _CONSTANTS[node.id]
    if isinstance(node, ast.BinOp) and type(node.op) in _BIN_OPS:
        return _BIN_OPS[type(node.op)](_eval(node.left, funcs), _eval(node.right, funcs))
    if isinstance(node, ast.UnaryOp) and type(node.op) in _UNARY_OPS:
        return _UNARY_OPS[type(node.op)](_eval(node.operand, funcs))
    if (
        isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id in funcs
        and len(node.args) == 1
        and not node.keywords
    ):
        return funcs[node.func.id](_eval(node.args[0], funcs))
    raise CalculatorError("Invalid expression")


def evaluate(expression, degrees=False):
    """Evaluate a text expression like '2^3 + sin(30) * ln(e)'."""
    expr = (
        expression.replace("^", "**")
        .replace("×", "*")
        .replace("÷", "/")
        .replace("√", "sqrt")
        .replace("π", "pi")
        .strip()
    )
    if not expr:
        raise CalculatorError("Empty expression")
    try:
        tree = ast.parse(expr, mode="eval")
        return _eval(tree, _functions(degrees))
    except CalculatorError:
        raise
    except SyntaxError:
        raise CalculatorError("Syntax error")
    except (ZeroDivisionError, OverflowError, ValueError):
        raise CalculatorError("Math error")


def format_result(value):
    """Clean display: 8.0 -> '8', 0.30000000000000004 -> '0.3'."""
    if abs(value) < 1e-12:
        return "0"
    if float(value).is_integer() and abs(value) < 1e15:
        return str(int(value))
    return f"{value:.10g}"
