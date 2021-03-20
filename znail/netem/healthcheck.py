"""Provides a collection of health checks used to determine the state of the system."""

import logging
import subprocess
from collections import OrderedDict

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


def perform_health_checks():
    """
    Run all health checks.

    Returns a dictionary containing the name of the health checks as keys
    and the verdict of the health check as values. Verdicts are represented
    as booleans.
    """
    return OrderedDict(
        [
            _check_that_the_netem_kernel_module_is_loaded(),
            _check_that_the_br_netfilter_kernel_module_is_loaded(),
            _check_that_the_bridge_interface_is_up(),
            _check_that_the_dnsmasq_server_is_running(),
        ]
    )


def _check_that_the_netem_kernel_module_is_loaded():
    return _run_check("The netem kernel module is loaded", "lsmod | grep sch_netem")


def _check_that_the_br_netfilter_kernel_module_is_loaded():
    return _run_check("The br_netfilter kernel module is loaded", "lsmod | grep sch_netem")


def _check_that_the_bridge_interface_is_up():
    return _run_check("The bridge interface is up", "cat /sys/class/net/br0/operstate | grep up")


def _check_that_the_dnsmasq_server_is_running():
    return _run_check("The dnsmasq service is running", "systemctl status dnsmasq --no-pager")


def _run_check(name, command):
    exit_code = 1
    try:
        logger.info("Running health check '{name}'".format(name=name))
        exit_code = subprocess.call(command, shell=True, timeout=1)
        logger.info("Health check '{name}' ok".format(name=name))
    except Exception as e:
        logger.debug(str(e), exc_info=True)
        logger.error("Health check '{name}' error: {error}".format(name=name, error=str(e)))
    return name, exit_code == 0
