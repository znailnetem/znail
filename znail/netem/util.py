import logging
import os
import subprocess
from textwrap import dedent

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

dnsmasq_overrides_file = os.getenv("DNSMASK_OVERRIDES_FILE", "/etc/dnsmasq.d/overrides")
hosts_file = os.getenv("HOSTS_FILE", "/etc/hosts")
hub_ctrl = os.getenv("HUB_CTRL_COMMAND", "hub-ctrl")
iptables = os.getenv("IPTABLES_COMMAND", "iptables")
shutdown = os.getenv("SHUTDOWN_COMMAND", "shutdown")
systemctl = os.getenv("SYSTEMCTL_COMMAND", "systemctl")
tc = os.getenv("TC_COMMAND", "tc")
tcpdump = os.getenv("TCPDUMP_COMMAND", "tcpdump")


def run_in_shell(command, timeout=1):
    try:
        logger.info("Running: {command}".format(command=command))
        exit_code = subprocess.check_call(command, shell=True, timeout=timeout)
        logger.info("Command exited with exit code {exit_code}".format(exit_code=exit_code))
    except Exception as e:
        logger.debug(str(e), exc_info=True)
        logger.error("Command error: {error}".format(error=str(e)))
        raise


def prepare_iptables():
    logger.info("Clearing IP tables NAT rules")
    run_in_shell("{iptables} -t nat -F".format(iptables=iptables))
    run_in_shell("{iptables} -t nat -A POSTROUTING -o eth0 -j MASQUERADE".format(iptables=iptables))


def reboot():
    run_in_shell("{shutdown} -r now".format(shutdown=shutdown))


def restore_hosts_file_to_default():
    logger.info("Restoring /etc/hosts file to default")
    run_in_shell(
        dedent(
            """\
    cat <<EOF> {hosts_file}
    127.0.0.1 localhost
    127.0.1.1 $(hostname)

    # The following lines are desirable for IPv6 capable hosts
    ::1     ip6-localhost ip6-loopback
    fe00::0 ip6-localnet
    ff00::0 ip6-mcastprefix
    ff02::1 ip6-allnodes
    ff02::2 ip6-allrouters
    ff02::3 ip6-allhosts
    EOF
    """.format(
                hosts_file=hosts_file
            )
        )
    )
