import logging

from .util import iptables, run_in_shell

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class IpRedirectDescriptor:
    def __init__(self, ip, port, destination_ip, destination_port, protocol):
        self.ip = ip
        self.port = port
        self.destination_ip = destination_ip
        self.destination_port = destination_port
        self.protocol = protocol

    @property
    def iptables_commandline(self):
        return (
            "-d {ip} -p {protocol} --dport {port} -j DNAT " "--to-destination {destination_ip}:{destination_port}"
        ).format(
            ip=self.ip,
            port=self.port,
            destination_ip=self.destination_ip,
            destination_port=self.destination_port,
            protocol=self.protocol,
        )

    def __lt__(self, other):
        return str(self.ip) + str(self.port) + str(self.destination_ip) + str(self.destination_port) + str(
            self.protocol
        ) < str(other.ip) + str(other.port) + str(other.destination_ip) + str(other.destination_port) + str(
            other.protocol
        )

    def __eq__(self, other):
        return self.ip == other.ip and self.port == other.port and self.protocol == other.protocol

    def __hash__(self):
        return hash(self.ip) ^ hash(self.port) ^ hash(self.protocol)

    def __str__(self):
        return "IP redirect {ip}:{port} -> {destination_ip}:{destination_port} ({protocol})".format(
            ip=self.ip,
            port=self.port,
            destination_ip=self.destination_ip,
            destination_port=self.destination_port,
            protocol=self.protocol,
        )


class IpRedirect:
    def __init__(self):
        self._redirects = []

    def apply(self, redirects):
        self.clear()
        self._redirects = redirects
        self._apply(redirects)

    @property
    def redirects(self):
        return self._redirects

    def clear(self):
        self._clear()
        self._redirects = []

    def _apply(self, redirects):
        for redirect in self._redirects:
            self._add_iptables_rule(redirect)

    def _clear(self):
        for redirect in self._redirects:
            self._remove_iptables_rule(redirect)

    def _add_iptables_rule(self, redirect):
        logger.info("Applying: {redirect}".format(redirect=str(redirect)))
        run_in_shell(
            " ".join(["{iptables} -t nat -A PREROUTING".format(iptables=iptables), redirect.iptables_commandline])
        )

    def _remove_iptables_rule(self, redirect):
        logger.info("Removing: {redirect}".format(redirect=str(redirect)))
        run_in_shell(
            " ".join(["{iptables} -t nat -D PREROUTING".format(iptables=iptables), redirect.iptables_commandline])
        )
