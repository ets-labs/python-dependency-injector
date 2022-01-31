"""`Aggregate` provider example."""

from dependency_injector import containers, providers


class ConfigReader:

    def __init__(self, path):
        self._path = path

    def read(self):
        print(f"Parsing {self._path} with {self.__class__.__name__}")
        ...


class YamlReader(ConfigReader):
    ...


class JsonReader(ConfigReader):
    ...


class Container(containers.DeclarativeContainer):

    config_readers = providers.Aggregate(
        yaml=providers.Factory(YamlReader),
        json=providers.Factory(JsonReader),
    )


if __name__ == "__main__":
    container = Container()

    yaml_reader = container.config_readers("yaml", "./config.yml")
    yaml_reader.read()  # Parsing ./config.yml with YamlReader

    json_reader = container.config_readers("json", "./config.json")
    json_reader.read()  # Parsing ./config.json with JsonReader
