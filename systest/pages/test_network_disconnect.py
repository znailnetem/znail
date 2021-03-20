from ..util import assert_has_title


def test_load_page(znail, disconnect_page):
    assert_has_title(disconnect_page.page, "Network Disconnect")


def test_enable_and_disable_network_disconnect(Znail, disconnect_page):
    with Znail() as znail:
        disconnect_page.toggle()
        disconnect_page.toggle()
    assert "-b 1 -d 2 -P 2 -p 0" in znail.stdout
    assert "-b 1 -d 2 -P 2 -p 1" in znail.stdout
