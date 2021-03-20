from ..util import assert_has_title

duplication_examples = [
    {
        "description": "Two switches misconfigured to broadcast the same traffic to the same address ",
        "value": "100",
    },
    {
        "description": "Duplication due to high packet loss causing dropped ACKs",
        "value": "5",
    },
    {
        "description": "Duplication due to minor packet loss causing dropped ACKs",
        "value": "2",
    },
]


def test_load_page(znail, packet_duplication_page):
    assert_has_title(packet_duplication_page.page, "Packet Duplication")


def test_set_packet_duplication(Znail, packet_duplication_page):
    with Znail() as znail:
        packet_duplication_page.set("10.1")
    assert "netem duplicate 10.1%" in znail.stdout


def test_get_packet_duplication(znail, packet_duplication_page):
    assert packet_duplication_page.get() is None


def test_set_and_get_packet_duplication(znail, packet_duplication_page):
    packet_duplication_page.set(10)
    assert packet_duplication_page.get() == 10


def test_clear_packet_duplication(znail, packet_duplication_page):
    packet_duplication_page.set(10)
    packet_duplication_page.set(None)
    assert packet_duplication_page.get() is None


def test_invalid_input(znail, packet_duplication_page):
    packet_duplication_page.set(-1, expect_success=False)


def test_examples(znail, packet_duplication_page):
    for example in duplication_examples:
        packet_duplication_page.set(example["value"])
        assert packet_duplication_page.get() == float(example["value"])


def test_clear_twice(znail, packet_duplication_page):
    packet_duplication_page.set()
    packet_duplication_page.set()
