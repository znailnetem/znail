from zaf.component.decorator import component, requires

from ..util import assert_danger_alert_is_shown, assert_has_title, assert_success_alert_is_shown

rate_examples = [
    {
        'description': 'A dialup modem',
        'kbit': 56,
        'latency': 1000,
        'burst': 10000,
    }, {
        'description': 'A slow ADSL connection',
        'kbit': 1536,
        'latency': 1000,
        'burst': 10000,
    }, {
        'description': 'A standard ADSL connection',
        'kbit': 4096,
        'latency': 1000,
        'burst': 10000,
    }, {
        'description': 'The max throughput of udp over 802.11b wifi',
        'kbit': 7270,
        'latency': 1000,
        'burst': 10000,
    }
]


@component
@requires(page_loader="PageLoader", args=['http://localhost/packet_rate_control'])
class PacketRateControlPage(object):

    def __init__(self, page_loader):
        self._page_loader = page_loader

    @property
    def page(self):
        return self._page_loader.page

    def get(self):
        page = self.page
        kbit_input = page.find_element_by_name('kbit')
        latency_milliseconds_input = page.find_element_by_name('latency_milliseconds')
        burst_bytes_input = page.find_element_by_name('burst_bytes')
        try:
            return (
                int(kbit_input.get_attribute('value')),
                int(latency_milliseconds_input.get_attribute('value')),
                int(burst_bytes_input.get_attribute('value')),
            )
        except ValueError:
            return None

    def set(self, kbit=None, latency_milliseconds=None, burst_bytes=None, expect_success=True):
        page = self.page
        kbit_input = page.find_element_by_name('kbit')
        latency_milliseconds_input = page.find_element_by_name('latency_milliseconds')
        burst_bytes_input = page.find_element_by_name('burst_bytes')
        kbit_input.clear()
        latency_milliseconds_input.clear()
        burst_bytes_input.clear()
        if kbit:
            kbit_input.send_keys(kbit)
        if latency_milliseconds:
            latency_milliseconds_input.send_keys(latency_milliseconds)
        if burst_bytes:
            burst_bytes_input.send_keys(burst_bytes)
        page.find_element_by_id('submit').click()
        if expect_success:
            assert_success_alert_is_shown(page)
        else:
            assert_danger_alert_is_shown(page)


@requires(znail="Znail")
@requires(packet_rate_control_page="PacketRateControlPage")
def test_load_page(znail, packet_rate_control_page):
    assert_has_title(packet_rate_control_page.page, 'Packet Rate Control')


@requires(packet_rate_control_page="PacketRateControlPage")
def test_set_packet_rate_control(Znail, packet_rate_control_page):
    with Znail() as znail:
        packet_rate_control_page.set(1, 2, 3)
    assert 'tbf rate 1kbit latency 2ms burst 3' in znail.stdout


@requires(znail="Znail")
@requires(packet_rate_control_page="PacketRateControlPage")
def test_get_packet_rate_control(znail, packet_rate_control_page):
    assert packet_rate_control_page.get() is None


@requires(znail="Znail")
@requires(packet_rate_control_page="PacketRateControlPage")
def test_set_and_get_packet_rate_control(znail, packet_rate_control_page):
    packet_rate_control_page.set(1, 2, 3)
    assert packet_rate_control_page.get() == (1, 2, 3)


@requires(znail="Znail")
@requires(packet_rate_control_page="PacketRateControlPage")
def test_clear_packet_rate_control(znail, packet_rate_control_page):
    packet_rate_control_page.set(1, 2, 3)
    packet_rate_control_page.set(None, None, None)
    assert packet_rate_control_page.get() is None


@requires(znail="Znail")
@requires(packet_rate_control_page="PacketRateControlPage")
def test_invalid_input(znail, packet_rate_control_page):
    packet_rate_control_page.set(-1, -1, -1, expect_success=False)


@requires(znail="Znail", instance=True)
@requires(packet_rate_control_page="PacketRateControlPage")
def test_examples(znail, packet_rate_control_page):
    for example in rate_examples:
        packet_rate_control_page.set(example['kbit'], example['latency'], example['burst'])
        assert packet_rate_control_page.get() == (
            example['kbit'], example['latency'], example['burst'])


@requires(znail="Znail", instance=True)
@requires(packet_rate_control_page="PacketRateControlPage")
def test_clear_twice(znail, packet_rate_control_page):
    packet_rate_control_page.set()
    packet_rate_control_page.set()
