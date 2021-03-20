from zaf.component.decorator import component, requires

from ..util import assert_danger_alert_is_shown, assert_has_title, assert_success_alert_is_shown
from .packet_delay import PacketDelayPage  # noqa


@component
@requires(page_loader="PageLoader", args=['http://localhost/network_whitelist'])
class WhitelistPage:

    def __init__(self, page_loader):
        self._page_loader = page_loader

    @property
    def page(self):
        return self._page_loader.page

    def add(self, ip_address, expect_success=True):
        page = self.page
        add_to_whitelist_input = page.find_element_by_name('add_to_whitelist')
        add_to_whitelist_input.clear()
        add_to_whitelist_input.send_keys(ip_address)
        page.find_element_by_id('submit').click()
        if expect_success:
            assert_success_alert_is_shown(page)
        else:
            assert_danger_alert_is_shown(page)

    def remove(self, ip_address):
        page = self.page
        page.find_element_by_id('remove_{ip_address}'.format(ip_address=ip_address)).click()
        assert_success_alert_is_shown(page)

    def get(self):
        page = self.page
        whitelist = []
        rows = page.find_elements_by_tag_name('tr')
        for row in rows[1:]:
            columns = row.find_elements_by_tag_name('td')
            whitelist.append(columns[0].text)
        return whitelist


@requires(znail="Znail")
@requires(whitelist_page="WhitelistPage")
def test_load_page(znail, whitelist_page):
    assert_has_title(whitelist_page.page, 'Network Whitelist')


@requires(packet_delay_page="PacketDelayPage")
@requires(whitelist_page="WhitelistPage")
def test_add_to_network_whitelist(Znail, packet_delay_page, whitelist_page):
    with Znail() as znail:
        whitelist_page.add('1.2.3.4')
        # The whitelist is applied lazily. We need to add some network emulation
        # like packet delay for the whitelist to be applied.
        packet_delay_page.set(10)
    assert 'filter add dev eth1 parent 1: protocol ip prio 1 u32 match ip dst 1.2.3.4/32 flowid 1:1' in znail.stdout
    assert 'filter add dev eth1 parent 1: protocol ip prio 1 u32 match ip src 1.2.3.4/32 flowid 1:1' in znail.stdout


@requires(znail="Znail")
@requires(whitelist_page="WhitelistPage")
def test_get_network_whitelist(znail, whitelist_page):
    assert len(whitelist_page.get()) == 0


@requires(znail="Znail")
@requires(whitelist_page="WhitelistPage")
def test_set_and_get_network_whitelist(znail, whitelist_page):
    whitelist_page.add('4.3.2.1')
    whitelist_page.add('1.2.3.4')
    assert whitelist_page.get() == ['1.2.3.4', '4.3.2.1']


@requires(znail="Znail")
@requires(whitelist_page="WhitelistPage")
def test_remove_item_from_network_whitelist(znail, whitelist_page):
    whitelist_page.add('1.2.3.4')
    whitelist_page.remove('1.2.3.4')
    assert len(whitelist_page.get()) == 0


@requires(znail="Znail")
@requires(whitelist_page="WhitelistPage")
def test_remove_multiple_items_from_network_whitelist(znail, whitelist_page):
    whitelist_page.add('4.3.2.1')
    whitelist_page.add('1.2.3.4')
    whitelist_page.remove('4.3.2.1')
    assert whitelist_page.get() == ['1.2.3.4']
    whitelist_page.remove('1.2.3.4')
    assert len(whitelist_page.get()) == 0


@requires(znail="Znail")
@requires(whitelist_page="WhitelistPage")
def test_invalid_input(znail, whitelist_page):
    znail, whitelist_page.add('a.b.c.d', expect_success=False)
