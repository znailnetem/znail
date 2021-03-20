import unittest
from textwrap import dedent
from unittest.mock import patch

from znail.netem.util import restore_hosts_file_to_default


class TestRestoreHostsFileToDefault(unittest.TestCase):
    def test_command_is_rendered_correctly(self):
        with patch("znail.netem.util.run_in_shell") as mock:
            restore_hosts_file_to_default()
            mock.assert_called_once_with(
                dedent(
                    """\
    cat <<EOF> /etc/hosts
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
    """
                )
            )
