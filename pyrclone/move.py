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

    def __init__(self, remote, cwd=None, queue=None, settings=None) -> None:
        settings = settings or {}
        prefix = settings.get("RCLONE_MOVE_KEY_PREFIX", defaults.RCLONE_MOVE_KEY_PREFIX)
        pattern = settings.get(
            "RCLONE_MOVE_KEY_PATTERN", defaults.RCLONE_MOVE_KEY_PATTERN
        )

        self.remote = remote
        self.cwd = os.path.abspath(cwd or os.getcwd())
        self.queue = queue or RedisQueue.from_settings(settings)
        self.key = pattern.format(remote=self.remote, prefix=prefix, cwd=self.cwd)

        # if verify_remote:
        #     Rclone().check_remote(remote)

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
