from pymongo import MongoClient
from pydantic import BaseModel
from dependency_injector import containers, providers
from applauncher.applauncher import Configuration


class MongoDBConfig(BaseModel):
    uri: str
    connect: bool = True


def get_default_database(client: MongoClient):
    return client.get_default_database()


class MongoDBContainer(containers.DeclarativeContainer):
    config = providers.Dependency(instance_of=MongoDBConfig)
    configuration = Configuration()
    mongo_client = providers.Singleton(
        MongoClient,
        host=configuration.provided.mongodb.uri,
        connect=configuration.provided.mongodb.connect
    )

    db = providers.Callable(
        get_default_database,
        mongo_client
    )


class MongoDBBundle:
    def __init__(self):
        self.config_mapping = {
            "mongodb": MongoDBConfig
        }

        self.injection_bindings = {"mongodb": MongoDBContainer}
