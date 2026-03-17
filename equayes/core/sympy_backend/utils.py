from typing import Any, Iterable

import sympy as sp
from sympy.core.numbers import Number
from sympy.parsing.sympy_parser import parse_expr
from sympy.printing.str import StrPrinter
from sympy.utilities.lambdify import lambdify


def replace_floats_in_print_order(
    expr, prefix="p", skip: Iterable = (0.5, -0.5, sp.Integer)
) -> tuple[sp.Expr, dict[sp.Symbol, sp.Number]]:
    """Replaces numeric constants in a SymPy expression with parameter symbols AND maintains the order of the printed sympy string,
    excluding constants given in skip.

    Args:
        expr (sp.Expr): The input SymPy expression containing numeric constants.
        prefix (str, optional): The prefix string used when generating new parameter symbols. Defaults to "p".
        skip (iterable): Constants given in expr to be ignored. Defaults to common exponents: (0.5, -0.5, sp.Integer))

    Returns:
        tuple: A tuple containing:
            - sympy.Expr: The new expression with constants replaced by symbols.
            - dict: A mapping dictionary of {sp.Symbol: original_numeric_value}.
    """

    class ParamPrinter(StrPrinter):
        def __init__(self):
            super().__init__()
            self.counter = 0
            self.param_values = {}

        def _print_Float(self, x):
            # keep selected constants unchanged
            # if any(x == s for s in skip):
            if isinstance(x, Number) and x in skip:
                return super()._print_Float(x)

            name = f"{prefix}{self.counter}"
            sym = sp.Symbol(name)
            self.param_values[sym] = x
            self.counter += 1
            return name

    printer = ParamPrinter()
    expr_text = printer.doprint(expr)

    # parse back to a SymPy expression
    local_dict = {**sp.__dict__}
    local_dict.update({s.name: s for s in expr.free_symbols})

    expr_with_params = parse_expr(
        expr_text, local_dict=local_dict, evaluate=False
    )  # todo: validate in test if correct parameters are skipped
    return expr_with_params, printer.param_values


def replace_constants_with_parameters(
    expr: sp.Expr, prefix="p", skip=(0.5, -0.5, sp.Integer)
) -> tuple[sp.Expr, dict[sp.Symbol, sp.Number]]:
    """Replaces numeric constants in a SymPy expression with parameter symbols, excluding constants given in skip.

    Args:
        expr (sp.Expr): The input SymPy expression containing numeric constants.
        prefix (str, optional): The prefix string used when generating new parameter symbols. Defaults to "p".
        skip (iterable): Constants given in expr to be ignored. Defaults to common exponents: (0.5, -0.5, sp.Integer))

    Returns:
        tuple: A tuple containing:
            - sympy.Expr: The new expression with constants replaced by symbols.
            - dict: A mapping dictionary of {sp.Symbol: original_numeric_value}.
    """
    param_values = {}
    counter = 0

    def _replace(e):
        nonlocal counter
        if isinstance(e, Number) and e not in skip:  # todo: validate in test if correct parameters are skipped
            s = sp.Symbol(f"{prefix}{counter}")
            param_values[s] = e
            counter += 1
            return s
        return e

    expr_with_params = expr.replace(lambda e: isinstance(e, Number), _replace)
    # param_values = dict(sorted(param_values.items(), key=lambda kv: str(kv[0]).lower()))

    return expr_with_params, param_values
