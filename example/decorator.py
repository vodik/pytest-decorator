import pytest
import inspect


class UseFixtures(object):
    def __init__(self, *args):
        self.args = args


class Decorator(object):
    pass


def decorator(outerfunc):
    class TestDecorator(Decorator):
        def __init__(self, func):
            self.__wrapped__ = func
            self.outerfunc = outerfunc
            self.outerargspec = inspect.getargspec(outerfunc).args

            self.fixtures = filter(lambda arg: arg != 'testbody',
                                   self.outerargspec[1:])
            self.usefixtures = UseFixtures(*self.fixtures)

    return TestDecorator


class DecoratedFunction(pytest.Function):
    def runtest(self):
        assert 'testbody' in self.obj.outerargspec
        funcargs = self.funcargs

        inner_args = {}
        for arg in self._fixtureinfo.argnames:
            inner_args[arg] = funcargs[arg]

        if inspect.isgeneratorfunction(self.obj.__wrapped__):
            def inner():
                for value in self.obj.__wrapped__(**inner_args):
                    yield value
        else:
            def inner():
                return self.obj.__wrapped__(**inner_args)

        outerargs = {'testbody': inner}
        for arg in self.obj.fixtures:
            outerargs[arg] = funcargs[arg]
        self.obj.outerfunc(**outerargs)
