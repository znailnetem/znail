from zaf.component.decorator import component, requires

from ..util import assert_danger_alert_is_shown, assert_has_title, assert_success_alert_is_shown

reordering_examples = [
    {
        'description': 'Some packets taking a slower path through the network',
        'ms': 100,
        'percent': "5",
    },
    {
        'description': 'Many packets taking an almost as good path through the network',
        'ms': 10,
        'percent': "50",
    },
]


@component
@requires(page_loader="PageLoader", args=['http://localhost/packet_reordering'])
class PacketReorderingPage:

    def __init__(self, page_loader):
        self._page_loader = page_loader

    @property
    def page(self):
        return self._page_loader.page

    def get(self):
        page = self.page
        milliseconds_input = page.find_element_by_name('milliseconds')
        percent_input = page.find_element_by_name('percent')
        try:
            return (
                int(milliseconds_input.get_attribute('value')),
                float(percent_input.get_attribute('value')),
            )
        except ValueError:
            return None

    def set(self, milliseconds=None, percent=None, expect_success=True):
        page = self.page
        milliseconds_input = page.find_element_by_name('milliseconds')
        percent_input = page.find_element_by_name('percent')
        milliseconds_input.clear()
        percent_input.clear()
        if milliseconds:
            milliseconds_input.send_keys(milliseconds)
        if percent:
            percent_input.send_keys(percent)
        page.find_element_by_id('submit').click()
        if expect_success:
            assert_success_alert_is_shown(page)
        else:
            assert_danger_alert_is_shown(page)


@requires(znail="Znail")
@requires(packet_reordering_page="PacketReorderingPage")
def test_load_page(znail, packet_reordering_page):
    assert_has_title(packet_reordering_page.page, 'Packet Reordering')


@requires(packet_reordering_page="PacketReorderingPage")
def test_set_packet_reordering(Znail, packet_reordering_page):
    with Znail() as znail:
        packet_reordering_page.set(100, "10.1")
    assert 'netem delay 100ms reorder 10.1%' in znail.stdout


@requires(znail="Znail")
@requires(packet_reordering_page="PacketReorderingPage")
def test_get_packet_reordering(znail, packet_reordering_page):
    assert packet_reordering_page.get() is None


@requires(znail="Znail")
@requires(packet_reordering_page="PacketReorderingPage")
def test_set_and_get_packet_reordering(znail, packet_reordering_page):
    packet_reordering_page.set(100, 10)
    assert packet_reordering_page.get() == (100, 10)


@requires(znail="Znail")
@requires(packet_reordering_page="PacketReorderingPage")
def test_clear_packet_reordering(znail, packet_reordering_page):
    packet_reordering_page.set(100, 10)
    packet_reordering_page.set(None, None)
    assert packet_reordering_page.get() is None


@requires(znail="Znail")
@requires(packet_reordering_page="PacketReorderingPage")
def test_invalid_input(znail, packet_reordering_page):
    packet_reordering_page.set(-1, -1, expect_success=False)


@requires(znail="Znail", instance=True)
@requires(packet_reordering_page="PacketReorderingPage")
def test_examples(znail, packet_reordering_page):
    for example in reordering_examples:
        packet_reordering_page.set(example['ms'], example['percent'])
        assert packet_reordering_page.get() == (example['ms'], float(example['percent']))


@requires(znail="Znail", instance=True)
@requires(packet_reordering_page="PacketReorderingPage")
def test_clear_twice(znail, packet_reordering_page):
    packet_reordering_page.set()
    packet_reordering_page.set()
