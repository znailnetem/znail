from ..util import assert_has_title

reordering_examples = [
    {
        "description": "Some packets taking a slower path through the network",
        "ms": 100,
        "percent": "5",
    },
    {
        "description": "Many packets taking an almost as good path through the network",
        "ms": 10,
        "percent": "50",
    },
]


def test_load_page(znail, packet_reordering_page):
    assert_has_title(packet_reordering_page.page, "Packet Reordering")


def test_set_packet_reordering(Znail, packet_reordering_page):
    with Znail() as znail:
        packet_reordering_page.set(100, "10.1")
    assert "netem delay 100ms reorder 10.1%" in znail.stdout


def test_get_packet_reordering(znail, packet_reordering_page):
    assert packet_reordering_page.get() is None


def test_set_and_get_packet_reordering(znail, packet_reordering_page):
    packet_reordering_page.set(100, 10)
    assert packet_reordering_page.get() == (100, 10)


def test_clear_packet_reordering(znail, packet_reordering_page):
    packet_reordering_page.set(100, 10)
    packet_reordering_page.set(None, None)
    assert packet_reordering_page.get() is None


def test_invalid_input(znail, packet_reordering_page):
    packet_reordering_page.set(-1, -1, expect_success=False)


def test_examples(znail, packet_reordering_page):
    for example in reordering_examples:
        packet_reordering_page.set(example["ms"], example["percent"])
        assert packet_reordering_page.get() == (example["ms"], float(example["percent"]))


def test_clear_twice(znail, packet_reordering_page):
    packet_reordering_page.set()
    packet_reordering_page.set()
