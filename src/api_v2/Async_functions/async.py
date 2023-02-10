from datetime import timedelta
from functools import wraps
from flask import current_app
from redis import Redis
from rq import Queue

q = Queue(connection=Redis(host='localhost', port=6379))


def async_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return current_app.ensure_sync(func)(*args, **kwargs)

    return wrapper


def async_decorator_queue(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        job = q.enqueue_in(timedelta(seconds=10), func)(*args, **kwargs)
    return wrapper
