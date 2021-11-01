"""`Configuration` provider alias example."""

from dependency_injector import containers, providers
from environs import Env


class Container(containers.DeclarativeContainer):

    config = providers.Configuration()


if __name__ == "__main__":
    env = Env()
    container = Container()

    with container.config.some_plugin_name as plugin:
        plugin.some_interval_ms.override(
            env.int(
                "SOME_INTERVAL_MS",
                default=30000,
            ),
        )

        with plugin.kafka as kafka:
            kafka.bootstrap_servers.override(
                env.list(
                    "KAFKA_BOOTSTRAP_SERVERS",
                    default=["kafka1", "kafka2"],
                ),
            )
            kafka.security_protocol.override(
                env.str(
                    "KAFKA_SECURITY_PROTOCOL",
                    default="SASL_SSL",
                ),
            )
