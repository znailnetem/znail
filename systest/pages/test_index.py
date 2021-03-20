from ..util import assert_has_title, assert_upgrade_alert_is_shown


def test_load_page(znail, index_page):
    assert_has_title(index_page.page, "Network Emulator")


def test_default_overview_page(znail, index_page):
    assert not any(index_page.overview.values())


def test_upgrade_alert_is_shown(Znail, index_page):
    with Znail(env={"ZNAIL_FORCE_UPDATE_STATE": "1"}):
        assert_upgrade_alert_is_shown(index_page.page)


def test_upgrade_alert_is_not_shown(znail, index_page):
    try:
        assert_upgrade_alert_is_shown(index_page.page)
    except AssertionError:
        pass
    else:
        raise AssertionError("Upgrade alert unexpectedly shown")


def test_overview_page_with_packet_delay_enabled(znail, index_page, packet_delay_page):
    packet_delay_page.set(milliseconds=10)
    overview = index_page.overview
    assert overview["Packet Delay"] is True
    assert len(list(filter(lambda item: item is True, overview.values()))) == 1


def test_overview_page_with_packet_loss_enabled(znail, index_page, packet_loss_page):
    packet_loss_page.set(percent=10)
    overview = index_page.overview
    assert overview["Packet Loss"] is True
    assert len(list(filter(lambda item: item is True, overview.values()))) == 1


def test_overview_page_with_packet_duplication_enabled(znail, index_page, packet_duplication_page):
    packet_duplication_page.set(percent=10)
    overview = index_page.overview
    assert overview["Packet Duplication"] is True
    assert len(list(filter(lambda item: item is True, overview.values()))) == 1


def test_overview_page_with_packet_reordering_enabled(znail, index_page, packet_reordering_page):
    packet_reordering_page.set(milliseconds=10, percent=10)
    overview = index_page.overview
    assert overview["Packet Reordering"] is True
    assert len(list(filter(lambda item: item is True, overview.values()))) == 1


def test_overview_page_with_packet_corruption_enabled(znail, index_page, packet_corruption_page):
    packet_corruption_page.set(percent=10)
    overview = index_page.overview
    assert overview["Packet Corruption"] is True
    assert len(list(filter(lambda item: item is True, overview.values()))) == 1


def test_overview_page_with_packet_rate_control_enabled(znail, index_page, packet_rate_control_page):
    packet_rate_control_page.set(kbit=10, latency_milliseconds=10, burst_bytes=10)
    overview = index_page.overview
    assert overview["Packet Rate Control"] is True
    assert len(list(filter(lambda item: item is True, overview.values()))) == 1


def test_overview_page_with_disconnect_enabled(znail, index_page, disconnect_page):
    disconnect_page.toggle()
    overview = index_page.overview
    assert overview["Disconnect"] is True
    assert len(list(filter(lambda item: item is True, overview.values()))) == 1


def test_overview_page_with_whitelist_enabled(znail, index_page, whitelist_page):
    whitelist_page.add(ip_address="1.2.3.4")
    overview = index_page.overview
    assert overview["Whitelist"] is True
    assert len(list(filter(lambda item: item is True, overview.values()))) == 1


def test_overview_page_with_dns_override_enabled(znail, index_page, dns_override_page):
    dns_override_page.add(ip_address="1.2.3.4", hostname="test.com")
    overview = index_page.overview
    assert overview["DNS Override"] is True
    assert len(list(filter(lambda item: item is True, overview.values()))) == 1


def test_overview_page_with_ip_redirect_enabled(znail, index_page, ip_redirect_page):
    ip_redirect_page.add(ip="2.3.4.5", port=8080, destination_ip="1.2.3.4", destination_port=80, protocol="tcp")
    overview = index_page.overview
    assert overview["IP Redirect"] is True
    assert len(list(filter(lambda item: item is True, overview.values()))) == 1


def test_overview_page_with_all_enabled(
    znail,
    index_page,
    packet_delay_page,
    packet_loss_page,
    packet_duplication_page,
    packet_reordering_page,
    packet_corruption_page,
    packet_rate_control_page,
    disconnect_page,
    whitelist_page,
    dns_override_page,
    ip_redirect_page,
):
    packet_delay_page.set(milliseconds=10)
    packet_loss_page.set(percent=10)
    packet_duplication_page.set(percent=10)
    packet_reordering_page.set(milliseconds=10, percent=10)
    packet_corruption_page.set(percent=10)
    packet_rate_control_page.set(kbit=10, latency_milliseconds=10, burst_bytes=10)
    disconnect_page.toggle()
    whitelist_page.add(ip_address="1.2.3.4")
    dns_override_page.add(ip_address="1.2.3.4", hostname="test.com")
    ip_redirect_page.add(ip="2.3.4.5", port=8080, destination_ip="1.2.3.4", destination_port=80, protocol="tcp")
    overview = index_page.overview
    assert all(overview.values())
