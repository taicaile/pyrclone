"""rclone move"""
import logging
import os

from . import defaults
from .queues import RedisQueue
from .rclone import Rclone

__all__ = ["RcloneMoveProducer", "RcloneMoveWorker"]

logger = logging.getLogger()


class RcloneMoveProducer:
    """rclone move"""

    def __init__(self, key, queue, cwd) -> None:

        self.key = key
        self.cwd = cwd
        self.queue = queue

    @classmethod
    def from_settings(cls, settings):
        """from settings"""
        cwd = os.path.abspath(settings.get("CWD", None) or os.getcwd())
        remote = settings.get("RCLONE_REMOTE")
        prefix = settings.get("RCLONE_MOVE_KEY_PREFIX", defaults.RCLONE_MOVE_KEY_PREFIX)
        pattern = settings.get(
            "RCLONE_MOVE_KEY_PATTERN", defaults.RCLONE_MOVE_KEY_PATTERN
        )
        key = pattern.format(remote=remote, prefix=prefix, cwd=cwd)
        queue = RedisQueue.from_settings(settings)

        return cls(key=key, queue=queue, cwd=cwd)

    def relative(self, filepath: str):
        if os.path.isabs(filepath):
            filepath = os.path.relpath(filepath, self.cwd)
        return filepath

    def push(self, filepath):
        self.queue.push(self.key, self.relative(filepath))


class RcloneMoveWorker:
    """rclone move"""

    def __init__(self, rclone=None) -> None:
        self.rclone = rclone or Rclone()
