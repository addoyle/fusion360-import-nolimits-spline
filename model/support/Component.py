from abc import ABC, abstractmethod


class Component(ABC):
    @staticmethod
    @abstractmethod
    def fromXml(node):
        pass
