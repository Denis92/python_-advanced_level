from Lesson_6.log.log_config import LogLevel
from functools import wraps

logger = LogLevel("config_task1_logg.ini", rotate_on=False)

def decor_log(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        wrapper.__dict__.update(func.__dict__)
        logger.info_log(f"function name = {wrapper.__name__}, function arguments = {args, kwargs}")
        return func(*args, **kwargs)
    return wrapper


@decor_log
def test_func(arg1, arg2):
    res = arg1 * arg2**2 + arg1
    return res

test_func(10, 15)