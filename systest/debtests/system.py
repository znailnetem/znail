import uuid


def test_startup_procedure(Znail):
    with Znail() as znail:
        pass
    assert '-t nat -F' in znail.stdout
    assert '-t nat -A POSTROUTING -o eth0 -j MASQUERADE' in znail.stdout
    assert 'qdisc del dev eth1 root' in znail.stdout


def test_mac_address_is_written_to_the_network_interfaces_file():
    mac_int = uuid.getnode()
    mac_hex = '{:012x}'.format(mac_int)
    mac_str = ':'.join(mac_hex[i:i + 2] for i in range(0, len(mac_hex), 2))
    with open('/etc/network/interfaces', 'r') as f:
        assert 'bridge_hw {mac_str}'.format(mac_str=mac_str) in ''.join(f.readlines())
