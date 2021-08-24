from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Configuration, Singleton, Factory

from shared.config import ApplicationSettings


class Container(DeclarativeContainer):
    config = Configuration()
    config.from_pydantic(ApplicationSettings())
