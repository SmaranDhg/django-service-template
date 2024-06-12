import logging
from functools import wraps
from typing import Callable


def exception_handle(
    func=None,
    return_on_exception=None,
    verbose=False,
    log_prefix: str = None,
    on_exception: Callable[[Exception], None] = None,
):
    """
    A decorater which invokes the function and catch the exception

    :param return_on_exception: return_on_exception
    :param verbose: log the exeption to console
    """

    def _wrapper_func(func):

        @wraps(func)
        def _invoker(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                if verbose:
                    logging.exception(f" {log_prefix}: {e}")
                    print(f"EXCEPTION: {log_prefix}: {e}")

                if on_exception and callable(on_exception):
                    on_exception(e)

                return return_on_exception
            

        return _invoker

    if func:
        return _wrapper_func(func)

    else:
        return _wrapper_func