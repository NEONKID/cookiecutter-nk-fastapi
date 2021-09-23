from dependency_injector.containers import copy
from dependency_injector.providers import Configuration, Singleton, Factory

from common.containers import BaseContainer


@copy(BaseContainer)
class Container(BaseContainer):
    ...
