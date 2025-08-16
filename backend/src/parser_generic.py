import abc
from typing import Any

class MedicalDocParser(metaclass = abc.ABCMeta):
    def __init__(self, text):
        self.text = text

    @abc.abstractmethod
    def parse(self) -> Any:
        pass