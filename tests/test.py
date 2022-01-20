"""test"""
from pyrclone.move import RcloneMoveProducer

rclone_move = RcloneMoveProducer("test")
rclone_move.push("test.txt")
