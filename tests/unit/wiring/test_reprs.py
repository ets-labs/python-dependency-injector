from dependency_injector.wiring import (
    Closing,
    InvariantModifier,
    Provide,
    ProvidedInstance,
    RequiredModifier,
    TypeModifier,
)


def test_type_modifier_repr() -> None:
    assert repr(TypeModifier(int)) == f"TypeModifier({int!r})"


def test_required_modifier_repr() -> None:
    assert repr(RequiredModifier()) == "RequiredModifier()"


def test_required_modifier_with_type_repr() -> None:
    type_modifier = TypeModifier(int)
    required_modifier = RequiredModifier(type_modifier)
    assert repr(required_modifier) == f"RequiredModifier({type_modifier!r})"


def test_invariant_modifier_repr() -> None:
    assert repr(InvariantModifier("test")) == "InvariantModifier('test')"


def test_provided_instance_repr() -> None:
    provided_instance = ProvidedInstance().test["attr"].call()

    assert repr(provided_instance) == "ProvidedInstance().test['attr'].call()"


def test_marker_repr() -> None:
    assert repr(Closing[Provide["test"]]) == "Closing[Provide['test']]"


def test_marker_with_modifier_repr() -> None:
    marker = Provide["test", RequiredModifier()]

    assert repr(marker) == "Provide['test', RequiredModifier()]"
