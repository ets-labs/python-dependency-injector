from dependency_injector import providers


class Animal:
    ...


class Cat(Animal):
    ...


# Test 1: to check Aggregate provider
provider1: providers.Aggregate[str] = providers.Aggregate(
    a=providers.Object("str1"),
    b=providers.Object("str2"),
)
provider_a_1: providers.Provider[str] = provider1.a
provider_b_1: providers.Provider[str] = provider1.b
val1: str = provider1("a")

provider1_set_non_string_keys: providers.Aggregate[str] = providers.Aggregate()
provider1_set_non_string_keys.set_providers({Cat: providers.Object("str")})
provider_set_non_string_1: providers.Provider[str] = provider1_set_non_string_keys.providers[Cat]

provider1_new_non_string_keys: providers.Aggregate[str] = providers.Aggregate(
    {Cat: providers.Object("str")},
)
factory_new_non_string_1: providers.Provider[str] = provider1_new_non_string_keys.providers[Cat]

provider1_no_explicit_typing = providers.Aggregate(a=providers.Object("str"))
provider1_no_explicit_typing_factory: providers.Provider[str] = provider1_no_explicit_typing.providers["a"]
provider1_no_explicit_typing_object: str = provider1_no_explicit_typing("a")
