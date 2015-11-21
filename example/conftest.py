from decorator import decorator, Decorator, DecoratedFunction


def pytest_pycollect_makeitem(collector, name, obj):
    try:
        if not isinstance(obj, Decorator):
            return
    except Exception:
        return

    return DecoratedFunction(name, collector)


def pytest_namespace():
    return {'decorator': decorator}
