import os

from zaf.component.decorator import component, requires

from ..util import assert_danger_alert_is_shown, assert_has_title, assert_success_alert_is_shown


@component
@requires(page_loader="PageLoader", args=['http://localhost/network_dnsoverride'])
class DnsOverridePage:

    def __init__(self, page_loader):
        self._page_loader = page_loader

    @property
    def page(self):
        return self._page_loader.page

    def add(self, ip_address, hostname, expect_success=True):
        page = self.page
        ip_address_input = page.find_element_by_name('ip_address')
        hostname_input = page.find_element_by_name('hostname')
        ip_address_input.clear()
        hostname_input.clear()
        if ip_address:
            ip_address_input.send_keys(ip_address)
        hostname_input.send_keys(hostname)
        page.find_element_by_id('submit').click()
        if expect_success:
            assert_success_alert_is_shown(page)
        else:
            assert_danger_alert_is_shown(page)

    def remove(self, ip_address, hostname):
        page = self.page
        page.find_element_by_id(
            'remove_{ip_address}_{hostname}'.format(
                ip_address=ip_address if ip_address else '', hostname=hostname)).click()
        assert_success_alert_is_shown(page)

    def get(self):
        page = self.page
        dnsoverride = []
        rows = page.find_elements_by_tag_name('tr')
        for row in rows[1:]:
            columns = row.find_elements_by_tag_name('td')
            dnsoverride.append((columns[0].text, columns[1].text))
        return dnsoverride


@requires(znail="Znail")
@requires(dns_override_page="DnsOverridePage")
def test_load_page(znail, dns_override_page):
    assert_has_title(dns_override_page.page, 'Network DNS Override')


@requires(dns_override_page="DnsOverridePage")
def test_add_to_network_dnsoverride(Znail, dns_override_page):
    with Znail():
        dns_override_page.add('1.2.3.4', 'abcd')


@requires(znail="Znail")
@requires(dns_override_page="DnsOverridePage")
def test_get_network_dnsoverride(znail, dns_override_page):
    assert len(dns_override_page.get()) == 0


@requires(znail="Znail")
@requires(dns_override_page="DnsOverridePage")
def test_set_and_get_network_dnsoverride(znail, dns_override_page):
    dns_override_page.add('4.3.2.1', 'host_a')
    dns_override_page.add('1.2.3.4', 'host_b')
    assert dns_override_page.get() == [('1.2.3.4', 'host_b'), ('4.3.2.1', 'host_a')]


@requires(znail="Znail")
@requires(dns_override_page="DnsOverridePage")
def test_remove_item_from_network_dnsoverride(znail, dns_override_page):
    dns_override_page.add('1.2.3.4', 'host_a')
    dns_override_page.remove('1.2.3.4', 'host_a')
    assert len(dns_override_page.get()) == 0


@requires(znail="Znail")
@requires(dns_override_page="DnsOverridePage")
def test_remove_multiple_items_from_network_dnsoverride(znail, dns_override_page):
    dns_override_page.add('4.3.2.1', 'host_b')
    dns_override_page.add('1.2.3.4', 'host_a')
    dns_override_page.remove('4.3.2.1', 'host_b')
    assert dns_override_page.get() == [('1.2.3.4', 'host_a')]
    dns_override_page.remove('1.2.3.4', 'host_a')
    assert len(dns_override_page.get()) == 0


@requires(znail="Znail")
@requires(dns_override_page="DnsOverridePage")
def test_invalid_input(znail, dns_override_page):
    dns_override_page.add('a.b.c.d', -1, expect_success=False)


@requires(znail="Znail")
@requires(dns_override_page="DnsOverridePage")
def test_configuration_is_written_to_disk(znail, dns_override_page):
    dns_override_page.add('1.2.3.4', 'somehost')
    dns_override_page.add(None, 'somehost')
    with open('/etc/hosts') as f:
        assert '1.2.3.4\tsomehost\n' in f.readlines()
    with open('/etc/dnsmasq.d/overrides') as f:
        assert 'address=/somehost/\n' in f.readlines()

    dns_override_page.remove(None, 'somehost')
    with open('/etc/hosts') as f:
        assert '1.2.3.4\tsomehost\n' in f.readlines()
    with open('/etc/dnsmasq.d/overrides') as f:
        assert 'address=/somehost/\n' not in f.readlines()

    dns_override_page.remove('1.2.3.4', 'somehost')
    with open('/etc/hosts') as f:
        assert '1.2.3.4\tsomehost\n' not in f.readlines()
    assert not os.path.isfile('/etc/dnsmasq.d/overrides')
