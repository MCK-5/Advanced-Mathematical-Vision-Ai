"""Evaluate simple arithmetic recognised from a handwritten expression."""

import ast
import operator
import re
from fractions import Fraction

BINARY_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
}


def solve_expression(expression: str) -> str:
    """Return an exact arithmetic result, or raise ValueError."""
    text = (expression.strip()
            .replace("×", "*").replace("÷", "/")
            .replace("−", "-").replace("²", "^2")
            .replace("³", "^3").replace("^", "**"))

    if not text or len(text) > 100 or not re.fullmatch(r"[0-9+\-*/().\s]+", text):
        raise ValueError("Only basic numeric arithmetic is supported.")

    def calculate(node, depth=0):
        if depth > 20:
            raise ValueError("Expression is too complex.")
        if isinstance(node, ast.Expression):
            return calculate(node.body, depth + 1)
        if isinstance(node, ast.Constant) and type(node.value) in (int, float):
            if abs(node.value) > 10**12:
                raise ValueError("Number is too large.")
            return Fraction(str(node.value))
        if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.UAdd, ast.USub)):
            value = calculate(node.operand, depth + 1)
            return -value if isinstance(node.op, ast.USub) else value
        if isinstance(node, ast.BinOp):
            left = calculate(node.left, depth + 1)
            right = calculate(node.right, depth + 1)
            if isinstance(node.op, ast.Pow):
                if right.denominator != 1 or abs(right.numerator) > 20:
                    raise ValueError("Only small integer powers are supported.")
                if left == 0 and right < 0:
                    raise ValueError("Division by zero.")
                result = left ** int(right)
            elif type(node.op) in BINARY_OPERATORS:
                if isinstance(node.op, ast.Div) and right == 0:
                    raise ValueError("Division by zero.")
                result = BINARY_OPERATORS[type(node.op)](left, right)
            else:
                raise ValueError("Unsupported operator.")
            if abs(result.numerator) > 10**30 or result.denominator > 10**30:
                raise ValueError("Result is too large.")
            return result
        raise ValueError("Unsupported expression.")

    try:
        answer = calculate(ast.parse(text, mode="eval"))
    except (SyntaxError, ZeroDivisionError) as exc:
        raise ValueError("Invalid arithmetic expression.") from exc
    return str(answer.numerator) if answer.denominator == 1 else str(answer)
