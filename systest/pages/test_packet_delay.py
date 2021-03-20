from ..util import assert_has_title

delay_examples = [
    {
        "description": "The average delay of a transatlantic connection",
        "value": 100,
    },
    {
        "description": "The average delay of a connection within the EU or the US",
        "value": 35,
    },
    {
        "description": "A satellite modem in the woods (terrible!)",
        "value": 600,
    },
]


def test_load_page(znail, packet_delay_page):
    assert_has_title(packet_delay_page.page, "Packet Delay")


def test_set_packet_delay(Znail, packet_delay_page):
    with Znail() as znail:
        packet_delay_page.set(10)
    assert "netem delay 10ms" in znail.stdout


def test_get_packet_delay(znail, packet_delay_page):
    assert packet_delay_page.get() is None


def test_set_and_get_packet_delay(znail, packet_delay_page):
    packet_delay_page.set(10)
    assert packet_delay_page.get() == 10


def test_clear_packet_delay(znail, packet_delay_page):
    packet_delay_page.set(10)
    packet_delay_page.set(None)
    assert packet_delay_page.get() is None


def test_invalid_input(znail, packet_delay_page):
    packet_delay_page.set(-1, expect_success=False)


def test_examples(znail, packet_delay_page):
    for example in delay_examples:
        packet_delay_page.set(example["value"])
        assert packet_delay_page.get() == example["value"]


def test_clear_twice(znail, packet_delay_page):
    packet_delay_page.set()
    packet_delay_page.set()
