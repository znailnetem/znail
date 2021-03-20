from ..util import assert_has_title

corruption_examples = [
    {
        "description": "DSL Modem with degrading filter",
        "value": "1",
    },
    {"description": "Poorly shielded cable next to an EMI source", "value": "5"},
]


def test_load_page(znail, packet_corruption_page):
    assert_has_title(packet_corruption_page.page, "Packet Corruption")


def test_set_packet_corruption(Znail, packet_corruption_page):
    with Znail() as znail:
        packet_corruption_page.set("10.1")
    assert "netem corrupt 10.1%" in znail.stdout


def test_get_packet_corruption(znail, packet_corruption_page):
    assert packet_corruption_page.get() is None


def test_set_and_get_packet_corruption(znail, packet_corruption_page):
    packet_corruption_page.set(10)
    assert packet_corruption_page.get() == 10


def test_clear_packet_corruption(znail, packet_corruption_page):
    packet_corruption_page.set(10)
    packet_corruption_page.set(None)
    assert packet_corruption_page.get() is None


def test_invalid_input(znail, packet_corruption_page):
    packet_corruption_page.set(-1, expect_success=False)


def test_examples(znail, packet_corruption_page):
    for example in corruption_examples:
        packet_corruption_page.set(example["value"])
        assert packet_corruption_page.get() == float(example["value"])


def test_clear_twice(znail, packet_corruption_page):
    packet_corruption_page.set()
    packet_corruption_page.set()
