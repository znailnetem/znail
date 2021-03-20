from ..util import assert_has_title


def test_load_page(znail, whitelist_page):
    assert_has_title(whitelist_page.page, "Network Whitelist")


def test_add_to_network_whitelist(Znail, packet_delay_page, whitelist_page):
    with Znail() as znail:
        whitelist_page.add("1.2.3.4")
        # The whitelist is applied lazily. We need to add some network emulation
        # like packet delay for the whitelist to be applied.
        packet_delay_page.set(10)
    assert "filter add dev eth1 parent 1: protocol ip prio 1 u32 match ip dst 1.2.3.4/32 flowid 1:1" in znail.stdout
    assert "filter add dev eth1 parent 1: protocol ip prio 1 u32 match ip src 1.2.3.4/32 flowid 1:1" in znail.stdout


def test_get_network_whitelist(znail, whitelist_page):
    assert len(whitelist_page.get()) == 0


def test_set_and_get_network_whitelist(znail, whitelist_page):
    whitelist_page.add("4.3.2.1")
    whitelist_page.add("1.2.3.4")
    assert whitelist_page.get() == ["1.2.3.4", "4.3.2.1"]


def test_remove_item_from_network_whitelist(znail, whitelist_page):
    whitelist_page.add("1.2.3.4")
    whitelist_page.remove("1.2.3.4")
    assert len(whitelist_page.get()) == 0


def test_remove_multiple_items_from_network_whitelist(znail, whitelist_page):
    whitelist_page.add("4.3.2.1")
    whitelist_page.add("1.2.3.4")
    whitelist_page.remove("4.3.2.1")
    assert whitelist_page.get() == ["1.2.3.4"]
    whitelist_page.remove("1.2.3.4")
    assert len(whitelist_page.get()) == 0


def test_invalid_input(znail, whitelist_page):
    znail, whitelist_page.add("a.b.c.d", expect_success=False)
