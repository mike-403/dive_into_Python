import json


def to_json(func):
    def wrapper(*args, **kwargs):
        return json.dumps(func(*args, **kwargs))
    wrapper.__name__ = func.__name__
    wrapper.__doc__ = func.__doc__
    return wrapper
