import functools

def _omit(json, arr):
    return {k: v for k, v in json.items() if k not in arr}


def omit(params):
    def decorator_omit(func):
        @functools.wraps(func)
        def func_wrapper(self, *args, **kwargs):
            json = func(self, *args, **kwargs)
            if isinstance(json, list):
                for i, dev in enumerate(json):
                    json[i] = _omit(dev, params)
                return json
            return _omit(json, params)
        return func_wrapper
    return decorator_omit
