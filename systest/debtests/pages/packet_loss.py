from zaf.component.decorator import component, requires

from ..util import assert_danger_alert_is_shown, assert_has_title, assert_success_alert_is_shown

loss_examples = [
    {
        'description':
        'A wifi connection on the same channel as all your neighbours in an densely populated apartment building',
        'value':
        "10",
    },
    {
        'description': 'Packet loss high enough for streamed video/voip to have problems',
        'value': "7.5",
    },
    {
        'description': 'A fairly high packet loss rate under which things should still work.',
        'value': "2.5",
    },
]


@component
@requires(page_loader="PageLoader", args=['http://localhost/packet_loss'])
class PacketLossPage(object):

    def __init__(self, page_loader):
        self._page_loader = page_loader

    @property
    def page(self):
        return self._page_loader.page

    def get(self):
        page = self.page
        percent_input = page.find_element_by_name('percent')
        try:
            return float(percent_input.get_attribute('value'))
        except ValueError:
            return None

    def set(self, percent=None, expect_success=True):
        page = self.page
        percent_input = page.find_element_by_name('percent')
        percent_input.clear()
        if percent:
            percent_input.send_keys(percent)
        page.find_element_by_id('submit').click()
        if expect_success:
            assert_success_alert_is_shown(page)
        else:
            assert_danger_alert_is_shown(page)


@requires(znail="Znail")
@requires(packet_loss_page="PacketLossPage")
def test_load_page(znail, packet_loss_page):
    assert_has_title(packet_loss_page.page, 'Packet Loss')


@requires(packet_loss_page="PacketLossPage")
def test_set_packet_loss(Znail, packet_loss_page):
    with Znail() as znail:
        packet_loss_page.set("10.1")
    assert 'netem loss 10.1%' in znail.stdout


@requires(znail="Znail")
@requires(packet_loss_page="PacketLossPage")
def test_get_packet_loss(znail, packet_loss_page):
    assert packet_loss_page.get() is None


@requires(znail="Znail")
@requires(packet_loss_page="PacketLossPage")
def test_set_and_get_packet_loss(znail, packet_loss_page):
    packet_loss_page.set(10)
    assert packet_loss_page.get() == 10


@requires(znail="Znail")
@requires(packet_loss_page="PacketLossPage")
def test_clear_packet_loss(znail, packet_loss_page):
    packet_loss_page.set(10)
    packet_loss_page.set(None)
    assert packet_loss_page.get() is None


@requires(znail="Znail")
@requires(packet_loss_page="PacketLossPage")
def test_invalid_input(znail, packet_loss_page):
    packet_loss_page.set(-1, expect_success=False)


@requires(znail="Znail", instance=True)
@requires(packet_loss_page="PacketLossPage")
def test_examples(znail, packet_loss_page):
    for example in loss_examples:
        packet_loss_page.set(example['value'])
        assert packet_loss_page.get() == float(example['value'])


@requires(znail="Znail", instance=True)
@requires(packet_loss_page="PacketLossPage")
def test_clear_twice(znail, packet_loss_page):
    packet_loss_page.set()
    packet_loss_page.set()
