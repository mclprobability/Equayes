from enum import Enum


class Constraint(Enum):
    """
    Constraint types for transforming unconstrained variables.

    Attributes
    ----------
    POSITIVE
        Enforces strict positivity (x > 0) via:
        x_constrained = exp(x_unconstrained)

    NEGATIVE
        Enforces strict negativity (x < 0) via:
        x_constrained = -exp(x_unconstrained)
    """

    POSITIVE = 1
    NEGATIVE = 2
