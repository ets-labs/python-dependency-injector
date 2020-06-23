from dependency_injector import containers, providers

CONFIG = {'core': {'value': 123}}
CONFIG2 = {'core': {'value': 124}}


def fn(value):
    return value

def fn_2(fn):
    fn()


class Core(containers.DeclarativeContainer):

    config = providers.Configuration('core')

    fn = providers.Callable(fn, value=config.value)



class Application(containers.DeclarativeContainer):
    """Application container."""

    config = providers.Configuration('config')

    core = Core(config=config.core)

    fd = providers.Callable(dict, fn=core.fn)


if __name__ == '__main__':
    application = Application(config=CONFIG)
    print(application.fd())

    application.config.override(CONFIG2)
    print(application.fd())
