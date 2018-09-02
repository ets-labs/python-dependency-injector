"""Dependency Injector Factory providers benchmark."""

import time

from dependency_injector import providers


N = 1000000


class A(object):
    pass


class B(object):
    pass


class C(object):
    pass


class Test(object):
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c


# Testing Factory provider

test_factory_provider = providers.Factory(
    Test,
    a=providers.Factory(A),
    b=providers.Factory(B),
    c=providers.Factory(C),
)

start = time.time()
for _ in range(1, N):
    test_factory_provider()
finish = time.time()

print(finish - start)


# Testing simple analog

def test_simple_factory_provider():
    return Test(a=A(), b=B(), c=C())


start = time.time()
for _ in range(1, N):
    test_simple_factory_provider()
finish = time.time()

print(finish - start)

# ------
# Result
# ------
#
# Python 2.7
#
# $ python tests/performance/factory_benchmark_1.py
# 0.87456202507
# 0.879760980606
#
# $ python tests/performance/factory_benchmark_1.py
# 0.949290990829
# 0.853044986725
#
# $ python tests/performance/factory_benchmark_1.py
# 0.964688062668
# 0.857432842255
#
# Python 3.7.0
#
# $ python tests/performance/factory_benchmark_1.py
# 1.1037120819091797
# 0.999565839767456
#
# $ python tests/performance/factory_benchmark_1.py
# 1.0855588912963867
# 1.0008318424224854
#
# $ python tests/performance/factory_benchmark_1.py
# 1.0706679821014404
# 1.0106139183044434
