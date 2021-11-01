"""Common test artifacts."""


class Example:
    def __init__(self, init_arg1=None, init_arg2=None, init_arg3=None, init_arg4=None):
        self.init_arg1 = init_arg1
        self.init_arg2 = init_arg2
        self.init_arg3 = init_arg3
        self.init_arg4 = init_arg4

        self.attribute1 = None
        self.attribute2 = None


class ExampleA(Example):
    pass


class ExampleB(Example):
    pass
