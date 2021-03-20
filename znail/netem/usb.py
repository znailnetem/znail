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


class Usb:
    def __init__(self):
        self._enabled = True

    def disable_all_usb_ports(self):
        """
        Disable all USB ports by powering them down.

        The built in network card remains unaffected by this.
        """
        logger.info("Disabling all USB ports")
        self._disable_usb_ports()
        self._enabled = False

    def enable_all_usb_ports(self):
        """Enable all USB ports."""
        logger.info("Enabling all USB ports")
        self._enable_usb_ports()
        self._enabled = True

    def _disable_usb_ports(self):
        run_in_shell("{hub_ctrl} -b 1 -d 2 -P 2 -p 0".format(hub_ctrl=hub_ctrl))

    def _enable_usb_ports(self):
        run_in_shell("{hub_ctrl} -b 1 -d 2 -P 2 -p 1".format(hub_ctrl=hub_ctrl))

    @property
    def enabled(self):
        return self._enabled
