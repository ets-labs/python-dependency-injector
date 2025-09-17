from dependency_injector.wiring import Provide, inject

missing_obj: object = Provide["missing"]


class TestMissingClass:
    obj: object = Provide["missing"]

    def method(self, obj: object = Provide["missing"]) -> object:
        return obj


@inject
def test_missing_function(obj: object = Provide["missing"]):
    return obj
