import logging

import click
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
    logger.info("Preparing system for use")
    prepare_iptables()
    restore_hosts_file_to_default()
    Usb().enable_all_usb_ports()
    Tc.adapter("eth1").clear()
    logger.info("Done preparing system for use")


@click.command()
@click.version_option()
@click.option("-h", "--host", type=str, default="0.0.0.0", help="Listen on address.")
@click.option("-p", "--port", type=int, default=80, help="Listen on this port.")
@click.option("-d", "--debug", is_flag=True, default=False, help="Run in debug mode.")
def main(host, port, debug):
    coloredlogs.install(level="DEBUG")
    _prepare_system_for_use()
    app.run(host=host, port=port, debug=debug, threaded=True)


if __name__ == "__main__":
    main()
