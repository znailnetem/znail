"""
Interact with the built-in USB hub on the Raspberry.

Uses "hub-ctrl.c" to control the power state of the USB hub.
https://github.com/codazoda/hub-ctrl.c

Apparently this type of operation is not supported on most USB hubs.
It turns out that we are in luck with the Raspberry Pi hardware (3B, 3B+).
"""

import logging

from .util import hub_ctrl, run_in_shell

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class Usb(object):

    def __init__(self):
        self._enabled = True

    def disable_all_usb_ports(self):
        """
        Disable all USB ports by powering them down.

        The built in network card remains unaffected by this.
        """
        logger.info('Disabling all USB ports')
        hub_id = self._get_hub_id()
        self._disable_usb_ports(hub_id)
        self._enabled = False

    def enable_all_usb_ports(self):
        """Enable all USB ports."""
        logger.info('Enabling all USB ports')
        hub_id = self._get_hub_id()
        self._enable_usb_ports(hub_id)
        self._enabled = True

    def _disable_usb_ports(self, hub_id):
        run_in_shell('{hub_ctrl} -h {hub_id} -P 2 -p 0'.format(hub_ctrl=hub_ctrl, hub_id=hub_id))

    def _enable_usb_ports(self, hub_id):
        run_in_shell('{hub_ctrl} -h {hub_id} -P 2 -p 1'.format(hub_ctrl=hub_ctrl, hub_id=hub_id))

    def _get_hub_id(self):
        with open('/proc/cpuinfo') as f:
            if 'a020d3' in f.read():
                logger.info('Running on a Raspberry Pi 3B+, hub_id is 1')
                return 1
            else:
                logger.info('Not running on a Raspberry Pi 3B+, hub_id is 0')
                return 0

    @property
    def enabled(self):
        return self._enabled
