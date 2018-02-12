import logging

import coloredlogs

import znail.ui.api  # noqa
import znail.ui.web  # noqa
from znail.netem.tc import Tc
from znail.netem.usb import Usb
from znail.netem.util import prepare_iptables, restore_hosts_file_to_default
from znail.ui import app

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


def _prepare_system_for_use():
    logger.info('Preparing system for use')
    prepare_iptables()
    restore_hosts_file_to_default()
    Usb().enable_all_usb_ports()
    Tc.adapter('eth1').clear()
    logger.info('Done preparing system for use')


def main():
    coloredlogs.install(level='DEBUG')
    _prepare_system_for_use()
    app.run(host='0.0.0.0', port=80, threaded=True)


if __name__ == '__main__':
    main()
