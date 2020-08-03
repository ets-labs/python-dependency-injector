"""`Configuration` provider dynamic item selector.

Details: https://github.com/ets-labs/python-dependency-injector/issues/274
"""

import dataclasses

from dependency_injector import providers


@dataclasses.dataclass
class Foo:
    option1: object
    option2: object


config = providers.Configuration(default={
    'target': 'A',
    'items': {
        'A': {
            'option1': 60,
            'option2': 80,
        },
        'B': {
            'option1': 10,
            'option2': 20,
        },
    },
})

foo = providers.Factory(
    Foo,
    option1=config.items[config.target].option1,
    option2=config.items[config.target].option2,
)


if __name__ == '__main__':
    config.target.from_env('TARGET')
    f = foo()
    print(f.option1, f.option2)


# $ TARGET=A python configuration_itemselector.py
# 60 80
# $ TARGET=B python configuration_itemselector.py
# 10 20
