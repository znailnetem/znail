from zaf.component.decorator import component, requires

from ..util import assert_has_title, assert_success_alert_is_shown
from .packet_delay import PacketDelayPage  # noqa


@component
@requires(page_loader='PageLoader', args=['http://localhost/network_disconnect'])
class DisconnectPage(object):

    def __init__(self, page_loader):
        self._page_loader = page_loader

    @property
    def page(self):
        return self._page_loader.page

    def toggle(self):
        page = self.page
        page.find_element_by_id('submit').click()
        assert_success_alert_is_shown(page)


@requires(znail='Znail')
@requires(disconnect_page='DisconnectPage')
def test_load_page(znail, disconnect_page):
    assert_has_title(disconnect_page.page, 'Network Disconnect')


@requires(disconnect_page='DisconnectPage')
def test_enable_and_disable_network_disconnect(Znail, disconnect_page):
    with Znail() as znail:
        disconnect_page.toggle()
        disconnect_page.toggle()
    assert '-h 0 -P 2 -p 0' in znail.stdout
    assert '-h 0 -P 2 -p 1' in znail.stdout
