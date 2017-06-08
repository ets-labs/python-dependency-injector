"""Test providers performance."""

import time
import gc

import dependency_injector.providers


class Tester(object):
    """Performance tester for provider module implementations."""

    def __init__(self, provider_modules, duration_factor):
        """Initializer."""
        self.provider_modules = provider_modules
        self.tests = [getattr(self, name)
                      for name in dir(self)
                      if name.startswith('test')]
        self.total_time = 0
        self.duration_factor = duration_factor

    def run(self):
        """Run all tests for all provider modules."""
        for module in self.provider_modules:
            print('\n')
            print('Running tests for module - "{module}":'
                  .format(module=module.__name__))

            gc.disable()
            for test in self.tests:
                start_time = time.time()
                test(module)
                self.total_time = time.time() - start_time
                print('Test "{test}" took - {time}'
                      .format(test=test.__name__,
                              time=self.total_time))
                gc.collect()

        gc.enable()
        print('\n')

    def test_raw_3_kw_injections(self, providers):
        """Test 3 keyword argument injections."""
        class A(object):
            pass

        class B(object):
            pass

        class C(object):
            pass

        class Test(object):
            def __init__(self, a, b, c):
                pass

        for x in xrange(int(5000000 * self.duration_factor)):
            Test(a=A(), b=B(), c=C())

    def test_factory_3_factory_kw_injections(self, providers):
        """Test factory with 3 keyword argument injections via factories."""
        class A(object):
            pass

        class B(object):
            pass

        class C(object):
            pass

        class Test(object):
            def __init__(self, a, b, c):
                pass

        a_factory = providers.Factory(A)
        b_factory = providers.Factory(B)
        c_factory = providers.Factory(C)
        test_factory = providers.Factory(Test,
                                         a=a_factory,
                                         b=b_factory,
                                         c=c_factory)
        for x in xrange(int(5000000 * self.duration_factor)):
            test_factory()

    def test_abstract_factory_3_factory_kw_injections(self, providers):
        """Test factory with 3 keyword argument injections via factories."""
        class A(object):
            pass

        class B(object):
            pass

        class C(object):
            pass

        class Test(object):
            def __init__(self, a, b, c):
                pass

        a_factory = providers.Factory(A)
        b_factory = providers.Factory(B)
        c_factory = providers.Factory(C)
        test_factory = providers.AbstractFactory(object)
        test_factory.override(providers.Factory(Test,
                                                a=a_factory,
                                                b=b_factory,
                                                c=c_factory))
        for x in xrange(int(5000000 * self.duration_factor)):
            test_factory()

    def test_factory_6_factory_kw_injections_0_context(self, providers):
        """Test factory with 6 keyword argument injections."""
        class Test(object):
            def __init__(self, a, b, c, d, e, f):
                pass

        test_factory = providers.Factory(Test, a=1, b=2, c=3, d=4, e=5, f=6)
        for x in xrange(int(5000000 * self.duration_factor)):
            test_factory()

    def test_factory_6_factory_kw_injections_1_context(self, providers):
        """Test factory with 6 keyword argument injections."""
        class Test(object):
            def __init__(self, a, b, c, d, e, f):
                pass

        test_factory = providers.Factory(Test, f=6)
        for x in xrange(int(5000000 * self.duration_factor)):
            test_factory(a=1, b=2, c=3, d=4, e=5)

    def test_factory_6_factory_kw_injections_3_context(self, providers):
        """Test factory with 6 keyword argument injections."""
        class Test(object):
            def __init__(self, a, b, c, d, e, f):
                pass

        test_factory = providers.Factory(Test, a=1, b=2, c=3)
        for x in xrange(int(5000000 * self.duration_factor)):
            test_factory(d=4, e=5, f=6)


if __name__ == '__main__':
    tester = Tester(
        provider_modules=[
            dependency_injector.providers,
        ],
        duration_factor=0.5)
    tester.run()
