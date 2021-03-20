from zaf.component.decorator import component, requires

from ..util import assert_danger_alert_is_shown, assert_has_title, assert_success_alert_is_shown

duplication_examples = [
    {
        'description':
        'Two switches misconfigured to broadcast the same traffic to the same address ',
        'value': "100",
    },
    {
        'description': 'Duplication due to high packet loss causing dropped ACKs',
        'value': "5",
    },
    {
        'description': 'Duplication due to minor packet loss causing dropped ACKs',
        'value': "2",
    },
]


@component
@requires(page_loader="PageLoader", args=['http://localhost/packet_duplication'])
class PacketDuplicationPage:

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
@requires(packet_duplication_page="PacketDuplicationPage")
def test_load_page(znail, packet_duplication_page):
    assert_has_title(packet_duplication_page.page, 'Packet Duplication')


@requires(packet_duplication_page="PacketDuplicationPage")
def test_set_packet_duplication(Znail, packet_duplication_page):
    with Znail() as znail:
        packet_duplication_page.set("10.1")
    assert 'netem duplicate 10.1%' in znail.stdout


@requires(znail="Znail")
@requires(packet_duplication_page="PacketDuplicationPage")
def test_get_packet_duplication(znail, packet_duplication_page):
    assert packet_duplication_page.get() is None


@requires(znail="Znail")
@requires(packet_duplication_page="PacketDuplicationPage")
def test_set_and_get_packet_duplication(znail, packet_duplication_page):
    packet_duplication_page.set(10)
    assert packet_duplication_page.get() == 10


@requires(znail="Znail")
@requires(packet_duplication_page="PacketDuplicationPage")
def test_clear_packet_duplication(znail, packet_duplication_page):
    packet_duplication_page.set(10)
    packet_duplication_page.set(None)
    assert packet_duplication_page.get() is None


@requires(znail="Znail")
@requires(packet_duplication_page="PacketDuplicationPage")
def test_invalid_input(znail, packet_duplication_page):
    packet_duplication_page.set(-1, expect_success=False)


@requires(znail="Znail", instance=True)
@requires(packet_duplication_page="PacketDuplicationPage")
def test_examples(znail, packet_duplication_page):
    for example in duplication_examples:
        packet_duplication_page.set(example['value'])
        assert packet_duplication_page.get() == float(example['value'])


@requires(znail="Znail", instance=True)
@requires(packet_duplication_page="PacketDuplicationPage")
def test_clear_twice(znail, packet_duplication_page):
    packet_duplication_page.set()
    packet_duplication_page.set()
