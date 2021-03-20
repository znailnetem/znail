from ..util import assert_has_title

rate_examples = [
    {
        "description": "A dialup modem",
        "kbit": 56,
        "latency": 1000,
        "burst": 10000,
    },
    {
        "description": "A slow ADSL connection",
        "kbit": 1536,
        "latency": 1000,
        "burst": 10000,
    },
    {
        "description": "A standard ADSL connection",
        "kbit": 4096,
        "latency": 1000,
        "burst": 10000,
    },
    {
        "description": "The max throughput of udp over 802.11b wifi",
        "kbit": 7270,
        "latency": 1000,
        "burst": 10000,
    },
]


def test_load_page(znail, packet_rate_control_page):
    assert_has_title(packet_rate_control_page.page, "Packet Rate Control")


def test_set_packet_rate_control(Znail, packet_rate_control_page):
    with Znail() as znail:
        packet_rate_control_page.set(1, 2, 3)
    assert "tbf rate 1kbit latency 2ms burst 3" in znail.stdout


def test_get_packet_rate_control(znail, packet_rate_control_page):
    assert packet_rate_control_page.get() is None


def test_set_and_get_packet_rate_control(znail, packet_rate_control_page):
    packet_rate_control_page.set(1, 2, 3)
    assert packet_rate_control_page.get() == (1, 2, 3)


def test_clear_packet_rate_control(znail, packet_rate_control_page):
    packet_rate_control_page.set(1, 2, 3)
    packet_rate_control_page.set(None, None, None)
    assert packet_rate_control_page.get() is None


def test_invalid_input(znail, packet_rate_control_page):
    packet_rate_control_page.set(-1, -1, -1, expect_success=False)


def test_examples(znail, packet_rate_control_page):
    for example in rate_examples:
        packet_rate_control_page.set(example["kbit"], example["latency"], example["burst"])
        assert packet_rate_control_page.get() == (example["kbit"], example["latency"], example["burst"])


def test_clear_twice(znail, packet_rate_control_page):
    packet_rate_control_page.set()
    packet_rate_control_page.set()
