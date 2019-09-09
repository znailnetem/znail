import logging
import socket
import subprocess
import time
from builtins import ConnectionRefusedError

from k2.cmd.run import RUN_COMMAND
from zaf.component.decorator import component
from zaf.extensions.extension import AbstractExtension, CommandExtension, get_logger_name

logger = logging.getLogger(get_logger_name('znail', 'znailcomponent'))
logger.addHandler(logging.NullHandler())


@CommandExtension('znailcomponent', extends=[RUN_COMMAND])
class ZnailExtension(AbstractExtension):

    def __init__(self, config, instances):

        @component()
        class Znail(object):

            def __init__(
                    self,
                    env=None,
                    override_iptables='echo',
                    override_tc='echo',
                    override_hub_ctrl='echo',
                    override_service='echo',
                    override_systemctl='echo'):

                znail_entry_point = subprocess.check_output(
                    ['which', 'znail'], universal_newlines=True).strip()

                self.env = env
                self.znail_command = (
                    'export IPTABLES_COMMAND={override_iptables} && '
                    'export TC_COMMAND={override_tc} && '
                    'export HUB_CTRL_COMMAND={hub_ctrl_command} && '
                    'export SERVICE_COMMAND={override_service} && '
                    'export SYSTEMCTL_COMMAND={override_systemctl} && '
                    'export ZNAIL_FORCE_INTERFACE_UP=1 && '
                    'sudo -E {entry_point}').format(
                        entry_point=znail_entry_point,
                        override_iptables=override_iptables,
                        hub_ctrl_command=override_hub_ctrl,
                        override_tc=override_tc,
                        override_service=override_service,
                        override_systemctl=override_systemctl)

            def _start_znail_process(self):
                logger.debug('Running znail command: {command}'.format(command=self.znail_command))
                env = self.env.copy() if self.env else {}
                env.update({'LC_ALL': 'C.UTF-8', 'LANG': 'C.UTF-8'})
                self.process = subprocess.Popen(
                    self.znail_command,
                    shell=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    env=env,
                    universal_newlines=True)

            def _wait_for_znail_process_to_become_ready(self, timeout=5):
                logger.debug('Waiting for Znail to start')
                start_time = time.time()
                while (time.time() - start_time) < timeout:
                    try:
                        s = socket.socket(socket.AF_INET)
                        s.connect(('localhost', 80))
                    except ConnectionRefusedError:
                        pass
                    else:
                        logger.debug('Znail is listening on port 80')
                        s.close()
                        break

            def __enter__(self):
                self._start_znail_process()
                self._wait_for_znail_process_to_become_ready()
                return self

            def __exit__(self, exc_type, exc_value, traceback):
                kill_process = subprocess.Popen(
                    'sudo killall -2 znail', stdout=subprocess.PIPE, shell=True)
                kill_process.wait()

                self.stdout, self.stderr = self.process.communicate()
                logger.debug('-------- stdout --------')
                for line in self.stdout.split('\n'):
                    logger.debug(line)
                logger.debug('-------- end stdout --------')
                logger.debug('-------- stderr --------')
                for line in self.stderr.split('\n'):
                    logger.debug(line)
                logger.debug('-------- end stderr --------')
