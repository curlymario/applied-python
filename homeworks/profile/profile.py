import time


def log(func, cls=None):
    if cls:
        func_name = '.'.join((cls.__name__, func.__name__))
    else:
        func_name = func.__name__

    def logged_func(*args, **kwargs):
        print('`{}` started'.format(func_name))
        start_time = time.time()
        result = func(*args, **kwargs)
        duration = time.time() - start_time
        print('`{}` finished in {}s'.format(func_name, duration))
        return result

    return logged_func


def profile(obj):
    if isinstance(obj, type):
        for method_name, method in obj.__dict__.items():
            if callable(method):
                setattr(obj, method_name, log(method, cls=obj))
        return obj
    elif callable(obj):
        return log(obj)


if __name__ == '__main__':
    @profile
    def foo():
        pass


    @profile
    class Bar:
        def __init__(self):
            pass


    foo()
    Bar()