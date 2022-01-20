"""Queue"""
from abc import ABC, abstractmethod


class Queue(ABC):
    """Queue"""

    @classmethod
    @abstractmethod
    def from_settings(cls, settings):
        """create backend from settings"""

    @abstractmethod
    def push(self, key, filepath):
        """push file to remote"""

    @abstractmethod
    def pop(self, key):
        """get file from remote"""
