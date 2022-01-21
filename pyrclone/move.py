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

    def __init__(self, key, queue, basedir) -> None:

        self.key = key
        self.basedir = basedir
        self.queue = queue

    @classmethod
    def from_settings(cls, settings):
        """from settings"""
        basedir = os.path.abspath(settings.get("BASEDIR", None) or os.getcwd())
        remote = settings.get("RCLONE_REMOTE")
        prefix = settings.get("RCLONE_MOVE_KEY_PREFIX", defaults.RCLONE_MOVE_KEY_PREFIX)
        pattern = settings.get(
            "RCLONE_MOVE_KEY_PATTERN", defaults.RCLONE_MOVE_KEY_PATTERN
        )
        key = pattern.format(remote=remote, prefix=prefix, basedir=basedir)
        queue = RedisQueue.from_settings(settings)

        return cls(key=key, queue=queue, basedir=basedir)

    def relative(self, filepath: str):
        if os.path.isabs(filepath):
            filepath = os.path.relpath(filepath, self.basedir)
        return filepath

    def push(self, filepath):
        self.queue.push(self.key, self.relative(filepath))


class RcloneMoveWorker:
    """rclone move"""

    def __init__(self, rclone=None) -> None:
        self.rclone = rclone or Rclone()
