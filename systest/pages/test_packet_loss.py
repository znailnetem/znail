from ..util import assert_has_title

loss_examples = [
    {
        "description": "A wifi connection on the same channel as all your neighbours in an densely populated apartment building",
        "value": "10",
    },
    {
        "description": "Packet loss high enough for streamed video/voip to have problems",
        "value": "7.5",
    },
    {
        "description": "A fairly high packet loss rate under which things should still work.",
        "value": "2.5",
    },
]


def test_load_page(znail, packet_loss_page):
    assert_has_title(packet_loss_page.page, "Packet Loss")


def test_set_packet_loss(Znail, packet_loss_page):
    with Znail() as znail:
        packet_loss_page.set("10.1")
    assert "netem loss 10.1%" in znail.stdout


def test_get_packet_loss(znail, packet_loss_page):
    assert packet_loss_page.get() is None


def test_set_and_get_packet_loss(znail, packet_loss_page):
    packet_loss_page.set(10)
    assert packet_loss_page.get() == 10


def test_clear_packet_loss(znail, packet_loss_page):
    packet_loss_page.set(10)
    packet_loss_page.set(None)
    assert packet_loss_page.get() is None


def test_invalid_input(znail, packet_loss_page):
    packet_loss_page.set(-1, expect_success=False)


def test_examples(znail, packet_loss_page):
    for example in loss_examples:
        packet_loss_page.set(example["value"])
        assert packet_loss_page.get() == float(example["value"])


def test_clear_twice(znail, packet_loss_page):
    packet_loss_page.set()
    packet_loss_page.set()
