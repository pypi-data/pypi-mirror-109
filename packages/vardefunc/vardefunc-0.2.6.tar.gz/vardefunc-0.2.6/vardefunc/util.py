"""Helper functions for the main functions in this module"""
from functools import partial, wraps
from typing import Any, Callable, List, Sequence, Tuple, Union

from string import ascii_lowercase
import vapoursynth as vs

core = vs.core


class FormatError(Exception):
    """Raised when a format of VideoNode object is not allowed."""
    pass  # noqa: PLW0107


def copy_docstring_from(source: Callable[..., Any]) -> Callable[..., Any]:
    """Decorator intended to copy the docstring from an other function

    Args:
        source (Callable[..., Any]): Source function.

    Returns:
        Callable[..., Any]: Function decorated
    """
    @wraps(source)
    def wrapper(func: Callable[..., Any]) -> Callable[..., Any]:
        func.__doc__ = source.__doc__
        return func
    return wrapper


def get_sample_type(clip: vs.VideoNode) -> vs.SampleType:
    """Returns the sample type of a VideoNode as an SampleType."""
    if clip.format is None:
        raise FormatError('Variable format not allowed!')
    return clip.format.sample_type


def load_operators_expr() -> List[str]:
    """Returns clip loads operators for std.Expr as a list of string."""
    abcd = list(ascii_lowercase)
    return abcd[-3:] + abcd[:-3]


def mae_expr(gray_only: bool = True) -> str:
    """Mean Absolute Error string to be integrated in std.Expr.

    Args:
        gray_only (bool, optional):
            If both actual observation and prediction are one plane each.
            Defaults to True.

    Returns:
        str: Expression.
    """
    return 'x y - abs' if gray_only else 'x a - abs y b - abs max z c - abs max'


def max_expr(n: int) -> str:  # noqa: PLC0103
    """Dynamic variable max string to be integrated in std.Expr.

    Args:
        n (int): Number of elements.

    Returns:
        str: Expression.
    """
    return 'x y max ' + ' max '.join(
        load_operators_expr()[i] for i in range(2, n)
    ) + ' max'


def pick_px_op(use_expr: bool,
               operations: Tuple[str, Union[Sequence[int], Sequence[float], int, float, Callable[..., Any]]]
               ):
    """[summary]

    Args:
        use_expr (bool): [description]
        operations (Tuple[str, Union[Sequence[int], Sequence[float], int, float, Callable[[], Any]]]): [description]

    Raises:
        ValueError: [description]
        ValueError: [description]

    Returns:
        partial[vs.VideoNode]: [description]
    """
    expr, lut = operations
    if use_expr:
        func = partial(core.std.Expr, expr=expr)
    else:
        if callable(lut):
            func = partial(core.std.Lut, function=lut)
        elif isinstance(lut, Sequence):
            if all(isinstance(x, int) for x in lut):
                func = partial(core.std.Lut, lut=lut)
            elif all(isinstance(x, float) for x in lut):
                func = partial(core.std.Lut, lutf=lut)
            else:
                raise ValueError('pick_px_operation: operations[1] is not a valid type!')
        elif isinstance(lut, int):
            func = partial(core.std.Lut, lut=lut)
        elif isinstance(lut, float):
            func = partial(core.std.Lut, lutf=lut)
        else:
            raise ValueError('pick_px_operation: operations[1] is not a valid type!')
    return func


def rmse_expr(gray_only: bool = True) -> str:
    """Root Mean Squared Error string to be integrated in std.Expr.

    Args:
        gray_only (bool, optional):
            If both actual observation and prediction are one plane each.
            Defaults to True.

    Returns:
        str: Expression.
    """
    return 'x y - dup * sqrt' if gray_only else 'x a - dup * sqrt y b - dup * sqrt max z c - dup * sqrt max'
