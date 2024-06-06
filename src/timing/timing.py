#!/usr/bin/env python3

from functools import wraps
from time import time

def timeit(f):
    @wraps(f)
    def wrap(*args, **kw):
        time_start = time()
        result = f(*args, **kw)
        time_end = time()
        time_diff = time_end - time_start
        print(f"func: [{f.__name__}] with args:[{args}, {kw}] took [{time_diff:.02f} sec]")
        return result
    return wrap
