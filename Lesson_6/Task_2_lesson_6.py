import sys
import inspect
from functools import wraps
from Lesson_6.log.log_config import LogLevel

logger = LogLevel("config_task2_logg.ini", rotate_on=False)
def log(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        wrapper.__dict__.update(func.__dict__)
        logger.info_log(f"{wrapper.__name__} was called from {sys._getframe(1).f_code.co_name}") #Первый вариент
        logger.info_log(f"{wrapper.__name__} was called from {inspect.stack()[1][3]}") #Второй вариант
        return func(*args, **kwargs)
    return wrapper

@log
def summ(a, b):
    return a + b

def d_summ(a, b):
    return summ(a, b)

d_summ(5, 2)
