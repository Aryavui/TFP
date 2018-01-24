"""
anoyfunc makes the function definition more wonderful.

Usage example:
def f(x):
    return x**(1/2)

def g(x, y):
    return x + 2*y

def h(x):
    return x**2 + x - 1

f or lambda x: x**(1/2) is equivalent to _**(1/2) or __**(1/2)
g or lambda x, y: x + 2*y is equivalent to _ + 2*_ or __ + 2*_
h or lambda x: x**2 + x - 1 is equivalent to __**2 + __ - 1

when you use this ,just write two lines of code:
from anoyfunc import underscore as _
from anoyfunc import uunderscore as __

So amazing!

Enjoy it!
"""
import random
import string
from itertools import repeat, count


def random_name():
    return "".join(random.choice(string.ascii_letters) for _ in range(14))


def fmap(format):
    def applyier(self, other):
        fmt = format.replace("self", self._format)
        if other.__class__ == self.__class__:
            return self.__class__(fmt.replace("other", other._format),
                                  dict(list(self._format_args.items()) + list(other._format_args.items())))
        elif isinstance(other, (Underscore, UUnderscore)):
            return UUnderscore(fmt.replace("other", other._format),
                                  dict(list(self._format_args.items()) + list(other._format_args.items())))
        else:
            name = random_name()
            return self.__class__(fmt.replace("other", "%%(%s)r" % name),
                                  dict(list(self._format_args.items()) + [(name, other)]))
    return applyier


def unary_fmap(format):
    def applyier(self):
        fmt = "(%s)" % format.replace("self", self._format)
        return self.__class__(fmt,
                              self._format_args)
    return applyier


class Underscore(object):

    __slots__ = "_format", "_format_args", "_func_from_format"

    def __init__(self, format_="_", format_args=None):
        self._format = format_
        self._format_args = format_args or {}
        self._func_from_format = eval(self._create_func_from_format())

    def __str__(self):
        str_func = self._create_func_from_format()
        return "<class 'anoyfunc.Underscore':a callable object.Roughly equivalent to function: %s>" % str_func

    def _create_func_from_format(self):
        args = map("".join, zip(repeat("x"), map(str, count(1))))
        l, r = [], self._format
        while r.count("_"):
            n = next(args)
            r = r.replace("_", n, 1)
            l.append(n)
        r = r % self._format_args
        return "lambda {left}: {right}".format(left=", ".join(l), right=r)
        # return "({left}) => {right}".format(left=", ".join(l), right=r)

    def __call__(self, *args):
        return self._func_from_format(*args)

    # 加减乘除（真除、地板除）模，次方
    __add__ = fmap("self + other")
    __sub__ = fmap( "self - other")
    __mul__ = fmap("self * other")
    __truediv__ = fmap("self / other")
    __floordiv__ = fmap( "self // other")
    __mod__ = fmap("self %% other")
    __pow__ = fmap("self ** other")

    # 负号、正号、非
    __neg__ = unary_fmap("-self")
    __pos__ = unary_fmap("+self")
    __invert__ = unary_fmap("~self")

    # 左移、右移
    __lshift__ = fmap("self << other")
    __rshift__ = fmap("self >> other")

    # 逻辑运算：与、或、异或
    __and__ = fmap("self & other")
    __or__ = fmap("self | other")
    __xor__ = fmap("self ^ other")

    # __radd__是自定义的类操作符，执行“右加”。解释器执行a+b，首先在查找a中有没有__add__操作符，
    # 如果a中没有定义，那么就在b中查找并执行__radd__。
    __radd__ = fmap("other + self")
    __rsub__ = fmap("other - self")
    __rmul__ = fmap("other * self")
    __rtruediv__ = fmap("other / self")
    __rfloordiv__ = fmap("other // self")
    __rmod__ = fmap("other %% self")
    __rpow__ = fmap("other ** self")

    __rlshift__ = fmap("other << self")
    __rrshift__ = fmap("other >> self")

    __rand__ = fmap("other & self")
    __ror__ = fmap("other | self")
    __rxor__ = fmap("other ^ self")

    # 关系运算：<, <=, >, >=, ==, !=
    __lt__ = fmap("self < other")
    __le__ = fmap("self <= other")
    __gt__ = fmap("self > other")
    __ge__ = fmap( "self >= other")
    __eq__ = fmap( "self == other")
    __ne__ = fmap("self != other")


class UUnderscore(Underscore):

    def __init__(self, format_="__", format_args=None):
        self._format = format_
        self._format_args = format_args or {}
        self._func_from_format = eval(self._create_func_from_format())

    def __str__(self):
        str_func = self._create_func_from_format()
        return "<class 'anoyfunc.UUnderscore':a callable object.Roughly equivalent to function: %s>" % str_func

    def _create_func_from_format(self):
        r = self._format.replace("__", 'x')
        args = map("".join, zip(repeat("x"), map(str, count(1))))
        l = []
        b = False
        while r.count("_"):
            b = True
            n = next(args)
            r = r.replace("_", n, 1)
            l.append(n)
        r = r % self._format_args
        if not b:
            return "lambda x: {r}".format(r=r)
        return "lambda x, {left}: {right}".format(left=", ".join(l), right=r)


underscore = Underscore()
uunderscore = UUnderscore()

if __name__ == '__main__':
    pass
