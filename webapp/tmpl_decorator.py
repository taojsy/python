from functools import wraps


def decorator_name(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # 1. code to execute BEFORE calling the decorated function.

        # 2. call the decorated function as required, returning it's
        #    results if needed.
        return func(*args, **kwargs)

        # 3. code to execute INSTEAD of calling the decorated function.

    return wrapper
