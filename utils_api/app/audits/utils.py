"""
Common utilities for audit functions.
"""


def resolve_value(financial_figure):
    """
    Resolves the true value of a financial figure by applying its scale_multiplier.
    """
    multiplier = financial_figure.scale_multiplier if hasattr(financial_figure, "scale_multiplier") and financial_figure.scale_multiplier else 1
    return financial_figure.value * multiplier