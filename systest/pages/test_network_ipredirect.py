from ..util import assert_has_title


def test_load_page(znail, ip_redirect_page):
    assert_has_title(ip_redirect_page.page, "Network IP Redirect")


def test_add_to_network_ip_redirect(Znail, ip_redirect_page):
    with Znail():
        ip_redirect_page.add("1.2.3.4", 80, "4.3.2.1", 8080, "UDP")


def test_get_network_ip_redirect(znail, ip_redirect_page):
    assert len(ip_redirect_page.get()) == 0


def test_set_and_get_network_ip_redirect(znail, ip_redirect_page):
    ip_redirect_page.add("1.2.3.4", 80, "4.3.2.1", 8080, "UDP")
    ip_redirect_page.add("4.3.2.1", 81, "1.2.3.4", 82, "TCP")
    assert ip_redirect_page.get() == [
        ("1.2.3.4", 80, "4.3.2.1", 8080, "udp"),
        ("4.3.2.1", 81, "1.2.3.4", 82, "tcp"),
    ]


def test_remove_item_from_network_ip_redirect(znail, ip_redirect_page):
    ip_redirect_page.add("1.2.3.4", 80, "4.3.2.1", 8080, "UDP")
    ip_redirect_page.remove("1.2.3.4", 80, "4.3.2.1", 8080, "udp")
    assert len(ip_redirect_page.get()) == 0


def test_remove_multiple_items_from_network_ip_redirect(znail, ip_redirect_page):
    ip_redirect_page.add("1.2.3.4", 80, "4.3.2.1", 8080, "UDP")
    ip_redirect_page.add("1.2.3.4", 80, "4.3.2.1", 8080, "TCP")
    ip_redirect_page.remove("1.2.3.4", 80, "4.3.2.1", 8080, "tcp")
    assert ip_redirect_page.get() == [("1.2.3.4", 80, "4.3.2.1", 8080, "udp")]
    ip_redirect_page.remove("1.2.3.4", 80, "4.3.2.1", 8080, "udp")
    assert len(ip_redirect_page.get()) == 0


def test_invalid_input(znail, ip_redirect_page):
    ip_redirect_page.add("a.b.c.d", -1, "a.b.c.d", -2, "tcp", expect_success=False)
