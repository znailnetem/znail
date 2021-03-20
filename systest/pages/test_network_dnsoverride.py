from ..util import assert_has_title


def test_load_page(znail, dns_override_page):
    assert_has_title(dns_override_page.page, "Network DNS Override")


def test_add_to_network_dnsoverride(Znail, dns_override_page):
    with Znail():
        dns_override_page.add("1.2.3.4", "abcd")


def test_get_network_dnsoverride(znail, dns_override_page):
    assert len(dns_override_page.get()) == 0


def test_set_and_get_network_dnsoverride(znail, dns_override_page):
    dns_override_page.add("4.3.2.1", "host_a")
    dns_override_page.add("1.2.3.4", "host_b")
    assert dns_override_page.get() == [("1.2.3.4", "host_b"), ("4.3.2.1", "host_a")]


def test_remove_item_from_network_dnsoverride(znail, dns_override_page):
    dns_override_page.add("1.2.3.4", "host_a")
    dns_override_page.remove("1.2.3.4", "host_a")
    assert len(dns_override_page.get()) == 0


def test_remove_multiple_items_from_network_dnsoverride(znail, dns_override_page):
    dns_override_page.add("4.3.2.1", "host_b")
    dns_override_page.add("1.2.3.4", "host_a")
    dns_override_page.remove("4.3.2.1", "host_b")
    assert dns_override_page.get() == [("1.2.3.4", "host_a")]
    dns_override_page.remove("1.2.3.4", "host_a")
    assert len(dns_override_page.get()) == 0


def test_invalid_input(znail, dns_override_page):
    dns_override_page.add("a.b.c.d", -1, expect_success=False)
