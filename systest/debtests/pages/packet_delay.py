from zaf.component.decorator import component, requires

from ..util import assert_danger_alert_is_shown, assert_has_title, assert_success_alert_is_shown

delay_examples = [
    {
        'description': 'The average delay of a transatlantic connection',
        'value': 100,
    }, {
        'description': 'The average delay of a connection within the EU or the US',
        'value': 35,
    }, {
        'description': 'A satellite modem in the woods (terrible!)',
        'value': 600,
    }
]


@component
@requires(page_loader="PageLoader", args=['http://localhost/packet_delay'])
class PacketDelayPage(object):

    def __init__(self, page_loader):
        self._page_loader = page_loader

    @property
    def page(self):
        return self._page_loader.page

    def get(self):
        page = self.page
        milliseconds_input = page.find_element_by_name('milliseconds')
        try:
            return int(milliseconds_input.get_attribute('value'))
        except ValueError:
            return None

    def set(self, milliseconds=None, expect_success=True):
        page = self.page
        milliseconds_input = page.find_element_by_name('milliseconds')
        milliseconds_input.clear()
        if milliseconds:
            milliseconds_input.send_keys(milliseconds)
        page.find_element_by_id('submit').click()
        if expect_success:
            assert_success_alert_is_shown(page)
        else:
            assert_danger_alert_is_shown(page)


@requires(znail="Znail")
@requires(packet_delay_page="PacketDelayPage")
def test_load_page(znail, packet_delay_page):
    assert_has_title(packet_delay_page.page, 'Packet Delay')


@requires(packet_delay_page="PacketDelayPage")
def test_set_packet_delay(Znail, packet_delay_page):
    with Znail() as znail:
        packet_delay_page.set(10)
    assert 'netem delay 10ms' in znail.stdout


@requires(znail="Znail")
@requires(packet_delay_page="PacketDelayPage")
def test_get_packet_delay(znail, packet_delay_page):
    assert packet_delay_page.get() is None


@requires(znail="Znail")
@requires(packet_delay_page="PacketDelayPage")
def test_set_and_get_packet_delay(znail, packet_delay_page):
    packet_delay_page.set(10)
    assert packet_delay_page.get() == 10


@requires(znail="Znail")
@requires(packet_delay_page="PacketDelayPage")
def test_clear_packet_delay(znail, packet_delay_page):
    packet_delay_page.set(10)
    packet_delay_page.set(None)
    assert packet_delay_page.get() is None


@requires(znail="Znail")
@requires(packet_delay_page="PacketDelayPage")
def test_invalid_input(znail, packet_delay_page):
    packet_delay_page.set(-1, expect_success=False)


@requires(znail="Znail", instance=True)
@requires(packet_delay_page="PacketDelayPage")
def test_examples(znail, packet_delay_page):
    for example in delay_examples:
        packet_delay_page.set(example['value'])
        assert packet_delay_page.get() == example['value']


@requires(znail="Znail", instance=True)
@requires(packet_delay_page="PacketDelayPage")
def test_clear_twice(znail, packet_delay_page):
    packet_delay_page.set()
    packet_delay_page.set()
