"""test"""
from pyrclone.move import RcloneMoveProducer

rclone_move = RcloneMoveProducer.from_settings({"RCLONE_REMOTE": "test"})
rclone_move.push("test.txt")
