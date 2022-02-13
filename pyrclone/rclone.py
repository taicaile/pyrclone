"""rclone wrapper"""
import logging
import os
import signal
import subprocess

logger = logging.getLogger()


def preexec_function():
    """disable keyboard interrupt"""
    # Ignore the SIGINT signal by setting the handler to the standard
    # signal handler SIG_IGN.
    signal.signal(signal.SIGINT, signal.SIG_IGN)


class Rclone:
    """rclone class"""

    def __init__(self, cfg_file=None, non_interruptable=True) -> None:
        """__init__"""
        self.non_interruptable = non_interruptable
        if cfg_file is None:
            self.cmd = "rclone"
        else:
            assert os.path.exists(cfg_file), f"{cfg_file} file not found"
            self.cmd = f"rclone --config '{os.path.abspath(cfg_file)}'"
        self.listremotes()

    def listremotes(self):
        """listremotes"""
        sub_cmd = "listremotes"
        self.run(sub_cmd)

    def check_remote(self, remote_path):
        """check_remote"""
        try:
            self.lsd(remote_path)
            return True
        except subprocess.CalledProcessError as e:
            logger.error(e)
            logger.error("rclone check remote failed")
            return False

    def lsd(self, remote_path):
        """lsd command"""
        sub_cmd = f"lsd {remote_path}"
        self.run(sub_cmd)

    def move(self, source, dest):
        """move command"""
        sub_cmd = f"move '{source}' '{dest}' -v"
        self.run(sub_cmd)

    def move_from_file(self, files_from, source, dest, transfers=4):
        """move from file"""
        # pylint: disable=line-too-long
        # rclone copy --files-from files-from.txt /home remote:backup
        sub_cmd = f"move --files-from '{files_from}' '{source}' '{dest}' -v --transfers {transfers}"
        self.run(sub_cmd)

    def sync(self, source, dest, transfers=4):
        sub_cmd = f"sync '{source}' '{dest}' -v --transfers {transfers}"
        self.run(sub_cmd)

    def run(self, sub_cmd):
        """run rclone command"""
        assert sub_cmd and isinstance(sub_cmd, str), "Command cannot be None"

        shell_cmd = self.cmd + " " + sub_cmd
        logger.debug(shell_cmd)
        # pylint: disable=subprocess-popen-preexec-fn
        with subprocess.Popen(
            shell_cmd,
            shell=True,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            preexec_fn=preexec_function if self.non_interruptable else None,
        ) as proc:
            for stdout_line in iter(proc.stdout.readline, ""):
                logger.info(stdout_line.strip("\n").strip())
            ret_code = proc.wait()
            if ret_code:
                raise subprocess.CalledProcessError(ret_code, proc.args)
