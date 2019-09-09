from zaf.component.decorator import component, requires

from ..util import assert_danger_alert_is_shown, assert_has_title, assert_success_alert_is_shown

corruption_examples = [
    {
        'description': 'DSL Modem with degrading filter',
        'value': "1",
    }, {
        'description': 'Poorly shielded cable next to an EMI source',
        'value': "5"
    }
]


@component
@requires(page_loader="PageLoader", args=['http://localhost/packet_corruption'])
class PacketCorruptionPage(object):

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
@requires(packet_corruption_page="PacketCorruptionPage")
def test_load_page(znail, packet_corruption_page):
    assert_has_title(packet_corruption_page.page, 'Packet Corruption')


@requires(packet_corruption_page="PacketCorruptionPage")
def test_set_packet_corruption(Znail, packet_corruption_page):
    with Znail() as znail:
        packet_corruption_page.set("10.1")
    assert 'netem corrupt 10.1%' in znail.stdout


@requires(znail="Znail")
@requires(packet_corruption_page="PacketCorruptionPage")
def test_get_packet_corruption(znail, packet_corruption_page):
    assert packet_corruption_page.get() is None


@requires(znail="Znail")
@requires(packet_corruption_page="PacketCorruptionPage")
def test_set_and_get_packet_corruption(znail, packet_corruption_page):
    packet_corruption_page.set(10)
    assert packet_corruption_page.get() == 10


@requires(znail="Znail")
@requires(packet_corruption_page="PacketCorruptionPage")
def test_clear_packet_corruption(znail, packet_corruption_page):
    packet_corruption_page.set(10)
    packet_corruption_page.set(None)
    assert packet_corruption_page.get() is None


@requires(znail="Znail")
@requires(packet_corruption_page="PacketCorruptionPage")
def test_invalid_input(znail, packet_corruption_page):
    packet_corruption_page.set(-1, expect_success=False)


@requires(znail="Znail")
@requires(packet_corruption_page="PacketCorruptionPage")
def test_examples(znail, packet_corruption_page):
    for example in corruption_examples:
        packet_corruption_page.set(example['value'])
        assert packet_corruption_page.get() == float(example['value'])


@requires(znail="Znail")
@requires(packet_corruption_page="PacketCorruptionPage")
def test_clear_twice(znail, packet_corruption_page):
    packet_corruption_page.set()
    packet_corruption_page.set()
