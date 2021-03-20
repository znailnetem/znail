from zaf.component.decorator import component, requires

from ..util import assert_danger_alert_is_shown, assert_has_title, assert_success_alert_is_shown


@component
@requires(page_loader="PageLoader", args=['http://localhost/network_ip_redirect'])
class IpRedirectPage:

    def __init__(self, page_loader):
        self._page_loader = page_loader

    @property
    def page(self):
        return self._page_loader.page

    def add(self, ip, port, destination_ip, destination_port, protocol, expect_success=True):
        page = self.page
        ip_input = page.find_element_by_name('ip')
        port_input = page.find_element_by_name('port')
        destination_ip_input = page.find_element_by_name('destination_ip')
        destination_port_input = page.find_element_by_name('destination_port')
        protocol_input = page.find_element_by_name('protocol')
        ip_input.clear()
        port_input.clear()
        destination_ip_input.clear()
        destination_port_input.clear()
        ip_input.send_keys(ip)
        port_input.send_keys(port)
        destination_ip_input.send_keys(destination_ip)
        destination_port_input.send_keys(destination_port)
        for option in protocol_input.find_elements_by_tag_name('option'):
            if option.text == protocol:
                option.click()
        page.find_element_by_id('submit').click()
        if expect_success:
            assert_success_alert_is_shown(page)
        else:
            assert_danger_alert_is_shown(page)

    def remove(self, ip, port, destination_ip, destination_port, protocol):
        page = self.page
        page.find_element_by_id(
            'remove_{ip}_{port}_{destination_ip}_{destination_port}_{protocol}'.format(
                ip=ip,
                port=port,
                destination_ip=destination_ip,
                destination_port=destination_port,
                protocol=protocol)).click()
        assert_success_alert_is_shown(page)

    def get(self):
        page = self.page
        ip_redirect = []
        rows = page.find_elements_by_tag_name('tr')
        for row in rows[1:]:
            columns = row.find_elements_by_tag_name('td')
            ip_redirect.append(
                (
                    columns[0].text, int(columns[1].text), columns[2].text, int(columns[3].text),
                    columns[4].text))
        return ip_redirect


@requires(znail="Znail")
@requires(ip_redirect_page="IpRedirectPage")
def test_load_page(znail, ip_redirect_page):
    assert_has_title(ip_redirect_page.page, 'Network IP Redirect')


@requires(ip_redirect_page="IpRedirectPage")
def test_add_to_network_ip_redirect(Znail, ip_redirect_page):
    with Znail():
        ip_redirect_page.add('1.2.3.4', 80, '4.3.2.1', 8080, 'UDP')


@requires(znail="Znail")
@requires(ip_redirect_page="IpRedirectPage")
def test_get_network_ip_redirect(znail, ip_redirect_page):
    assert len(ip_redirect_page.get()) == 0


@requires(znail="Znail")
@requires(ip_redirect_page="IpRedirectPage")
def test_set_and_get_network_ip_redirect(znail, ip_redirect_page):
    ip_redirect_page.add('1.2.3.4', 80, '4.3.2.1', 8080, 'UDP')
    ip_redirect_page.add('4.3.2.1', 81, '1.2.3.4', 82, 'TCP')
    assert ip_redirect_page.get() == [
        ('1.2.3.4', 80, '4.3.2.1', 8080, 'udp'),
        ('4.3.2.1', 81, '1.2.3.4', 82, 'tcp'),
    ]


@requires(znail="Znail")
@requires(ip_redirect_page="IpRedirectPage")
def test_remove_item_from_network_ip_redirect(znail, ip_redirect_page):
    ip_redirect_page.add('1.2.3.4', 80, '4.3.2.1', 8080, 'UDP')
    ip_redirect_page.remove('1.2.3.4', 80, '4.3.2.1', 8080, 'udp')
    assert len(ip_redirect_page.get()) == 0


@requires(znail="Znail")
@requires(ip_redirect_page="IpRedirectPage")
def test_remove_multiple_items_from_network_ip_redirect(znail, ip_redirect_page):
    ip_redirect_page.add('1.2.3.4', 80, '4.3.2.1', 8080, 'UDP')
    ip_redirect_page.add('1.2.3.4', 80, '4.3.2.1', 8080, 'TCP')
    ip_redirect_page.remove('1.2.3.4', 80, '4.3.2.1', 8080, 'tcp')
    assert ip_redirect_page.get() == [('1.2.3.4', 80, '4.3.2.1', 8080, 'udp')]
    ip_redirect_page.remove('1.2.3.4', 80, '4.3.2.1', 8080, 'udp')
    assert len(ip_redirect_page.get()) == 0


@requires(znail="Znail")
@requires(ip_redirect_page="IpRedirectPage")
def test_invalid_input(znail, ip_redirect_page):
    ip_redirect_page.add('a.b.c.d', -1, 'a.b.c.d', -2, 'tcp', expect_success=False)
