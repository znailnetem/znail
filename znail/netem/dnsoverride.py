"""Provides facilities for redirecting outgoing DNS traffic to a local DNS server."""

import logging
import os
from pprint import pformat

from python_hosts import Hosts, HostsEntry

from .util import iptables, restore_hosts_file_to_default, run_in_shell, systemctl, dnsmasq_overrides_file

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class DnsOverrideDescriptor:
    def __init__(self, hostname, ip_address=None):
        self._hostname = hostname
        self._ip_address = ip_address

    @property
    def hostname(self):
        return self._hostname

    @property
    def ip_address(self):
        return self._ip_address

    def __lt__(self, other):
        return str(self._hostname) + str(self._ip_address) < str(other._hostname) + str(other._hostname)

    def __eq__(self, other):
        return self._hostname == other.hostname and self._ip_address == other.ip_address

    def __hash__(self):
        return hash(self._hostname) ^ hash(self._ip_address)

    def __str__(self):
        return "DNS override {hostname} -> {ip_address}".format(
            hostname=self._hostname, ip_address="(nothing)" if not self._ip_address else self._ip_address
        )


class DnsOverrides:
    def __init__(self):
        self._override_descriptors = []

    def apply(self, override_descriptors):
        try:
            self._override_descriptors = override_descriptors
            self._apply(override_descriptors)
        except Exception as e:
            logger.debug(str(e), exc_info=True)

    @property
    def overrides(self):
        return self._override_descriptors

    def clear(self):
        self._override_descriptors = []
        self._clear()

    def _apply(self, override_descriptors):
        self._redirect_all_dns_traffic_to_local_server()
        self._apply_hosts_file_overrides()
        self._apply_dnsmasq_config_overrides()
        self._reload_dnsmasq_service()

    def _clear(self):
        restore_hosts_file_to_default()
        self._clear_dnsmasq_config_overrides()
        self._reload_dnsmasq_service()

    def _reload_dnsmasq_service(self):
        run_in_shell("{systemctl} reset-failed dnsmasq".format(systemctl=systemctl))
        run_in_shell("{systemctl} restart dnsmasq".format(systemctl=systemctl))

    def _redirect_all_dns_traffic_to_local_server(self):
        run_in_shell(
            (
                "{iptables} -t nat -D PREROUTING -p udp --dport 53 "
                "-j DNAT --to-destination $(hostname -I | awk '{{print $1}}') || true"
            ).format(iptables=iptables)
        )
        run_in_shell(
            (
                "{iptables} -t nat -A PREROUTING -p udp --dport 53 "
                "-j DNAT --to-destination $(hostname -I | awk '{{print $1}}'):53"
            ).format(iptables=iptables)
        )

    def _apply_hosts_file_overrides(self):
        restore_hosts_file_to_default()

        logger.info("Applying hosts file overrides")
        overrides = filter(lambda o: bool(o.ip_address), self._override_descriptors)
        logger.info(pformat(overrides))

        self._write_hosts_file(overrides)

    def _write_hosts_file(self, overrides):
        hosts_file = Hosts(path="/etc/hosts")
        hosts_file.add(
            [
                HostsEntry(entry_type="ipv4", address=override.ip_address, names=[override.hostname])
                for override in overrides
            ]
        )
        hosts_file.write()

    def _apply_dnsmasq_config_overrides(self):
        self._clear_dnsmasq_config_overrides()

        logger.info("Applying dnsmasq config overrides")
        overrides = filter(lambda o: not bool(o.ip_address), self._override_descriptors)
        logger.info(pformat(overrides))

        self._write_dnsmasq_config_file(overrides)

    def _write_dnsmasq_config_file(self, overrides):
        with open(dnsmasq_overrides_file, "w") as f:
            f.writelines(["address=/{hostname}/\n".format(hostname=override.hostname) for override in overrides])

    def _clear_dnsmasq_config_overrides(self):
        logger.info("Cleaning dnsmasq config overrides")
        try:
            os.unlink(dnsmasq_overrides_file)
        except Exception:
            pass
