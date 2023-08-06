from abc import ABC
from abc import abstractmethod


class Query(ABC):

    @abstractmethod
    def save(self, data):
        pass

    @abstractmethod
    def get(self, data):
        pass

    @abstractmethod
    def filter(self, data):
        pass

    @abstractmethod
    def update(self, data):
        pass

    @abstractmethod
    def delete(self, data):
        pass
