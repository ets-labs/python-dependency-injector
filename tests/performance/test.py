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

#     def test_simple_object(self, providers):
#         """Test simple object's creation."""
#         class Test(object):
#             pass
#
#         for x in xrange(int(5000000 * self.duration_factor)):
#             Test()
#
#     def test_simple_object_factory(self, providers):
#         """Test simple object's factory."""
#         class Test(object):
#             pass
#
#         test_factory = providers.Factory(Test)
#         for x in xrange(int(5000000 * self.duration_factor)):
#             test_factory()
#
#     def test_3_ctx_positional_injections(self, providers):
#         """Test factory with 3 context positional injections."""
#         class Test(object):
#             def __init__(self, a, b, c):
#                 pass
#
#         for x in xrange(int(5000000 * self.duration_factor)):
#             Test(1, 2, 3)
#
#     def test_factory_3_ctx_positional_injections(self, providers):
#         """Test factory with 3 context positional injections."""
#         class Test(object):
#             def __init__(self, a, b, c):
#                 pass
#
#         test_factory = providers.Factory(Test)
#         for x in xrange(int(5000000 * self.duration_factor)):
#             test_factory(1, 2, 3)

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

    def test_overridden_factory_3_factory_kw_injections(self, providers):
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
        test_factory = providers.Factory(object)
        test_factory.override(providers.Factory(Test,
                                                a=a_factory,
                                                b=b_factory,
                                                c=c_factory))
        for x in xrange(int(5000000 * self.duration_factor)):
            test_factory()

#     def test_factory_subcls_3_factory_subcls_kw_injections(self, providers):
#         """Test factory with 3 keyword argument injections via factories."""
#         class MyFactory(providers.Factory):
#             pass
#
#         class A(object):
#             pass
#
#         class B(object):
#             pass
#
#         class C(object):
#             pass
#
#         class Test(object):
#             def __init__(self, a, b, c):
#                 pass
#
#         a_factory = MyFactory(A)
#         b_factory = MyFactory(B)
#         c_factory = MyFactory(C)
#         test_factory = MyFactory(Test,
#                                  a=a_factory,
#                                  b=b_factory,
#                                  c=c_factory)
#         for x in xrange(int(5000000 * self.duration_factor)):
#             test_factory()

#     def test_singleton(self, providers):
#         """Test factory with 3 keyword argument injections via factories."""
#         class Test(object):
#             def __init__(self):
#                 pass
#
#         test_factory = providers.Singleton(Test)
#         for x in xrange(int(5000000 * self.duration_factor)):
#             test_factory()
#
#     def test_singleton_subcls(self, providers):
#         """Test factory with 3 keyword argument injections via factories."""
#         class MySingleton(providers.Singleton):
#             pass
#
#         class Test(object):
#             pass
#
#         test_factory = MySingleton(Test)
#         for x in xrange(int(5000000 * self.duration_factor)):
#             test_factory()


if __name__ == '__main__':
    tester = Tester(
        provider_modules=[
            dependency_injector.providers,
        ],
        duration_factor=0.5)
    tester.run()
