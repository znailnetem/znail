"""
Interact with the "tcpdump" command line utility.

For more information about "tcpdump", please see:
https://www.tcpdump.org/manpages/tcpdump.1.html
"""
import logging
import subprocess

from .util import tcpdump

logger = logging.getLogger(__name__)


class TcpDump:
    def __init__(self, adapter):
        self._adapter = adapter

    def __enter__(self):
        command = [tcpdump, "-i", self._adapter, "-s", "0", "-U", "-n", "-w", "-"]
        proc = subprocess.Popen(command, stdout=subprocess.PIPE)

        def generator():
            logger.info("Start tcpdump for {adapter}".format(adapter=self._adapter))
            try:
                while True:
                    yield proc.stdout.read(128)
            except Exception as e:
                logger.info(str(e))
            finally:
                proc.terminate()
                logger.info("Stop tcpdump for {adapter}".format(adapter=self._adapter))

        return generator()

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
