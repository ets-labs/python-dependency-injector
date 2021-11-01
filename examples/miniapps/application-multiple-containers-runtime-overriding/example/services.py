"""Services module."""


class ConfigService:
    def __init__(self, config):
        self._config = config

    def build(self):
        self._config.from_dict({"default": {"db_path": "~/test"}})
