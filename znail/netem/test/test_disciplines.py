import unittest

from ..disciplines import (
    PacketCorruption,
    PacketDelay,
    PacketDuplication,
    PacketLoss,
    PacketReordering,
    QueueingDiscipline,
    RateControl,
)


def test_queueing_discipline():
    qd = QueueingDiscipline("name", "discipline")
    assert qd.name == "name"
    assert qd.discipline == "discipline"


class TestPacketDelay(unittest.TestCase):
    def test_packet_delay(self):
        qd = PacketDelay(1000)
        assert qd.name == "delay"
        assert qd.milliseconds == 1000
        assert qd.discipline == "netem delay 1000ms"

    def test_equality(self):
        assert PacketDelay(1000) == PacketDelay(1000)

    def test_inequality(self):
        assert PacketDelay(1000) != PacketDelay(2000)


class TestPacketLoss(unittest.TestCase):
    def test_packet_loss(self):
        qd = PacketLoss(50)
        assert qd.name == "loss"
        assert qd.percent == 50
        assert qd.discipline == "netem loss 50%"

    def test_equality(self):
        assert PacketLoss(50) == PacketLoss(50)

    def test_inequality(self):
        assert PacketLoss(50) != PacketLoss(100)


class TestPacketDuplication(unittest.TestCase):
    def test_packet_duplication(self):
        qd = PacketDuplication(50)
        assert qd.name == "duplicate"
        assert qd.percent == 50
        assert qd.discipline == "netem duplicate 50%"

    def test_equality(self):
        assert PacketDuplication(50) == PacketDuplication(50)

    def test_inequality(self):
        assert PacketDuplication(50) != PacketDuplication(100)


class TestPacketReordering(unittest.TestCase):
    def test_packet_reordering(self):
        qd = PacketReordering(50, 1000)
        assert qd.name == "reorder"
        assert qd.percent == 50
        assert qd.milliseconds == 1000
        assert qd.discipline == "netem delay 1000ms reorder 50%"

    def test_equality(self):
        assert PacketReordering(50, 1000) == PacketReordering(50, 1000)

    def test_inequality(self):
        assert PacketReordering(50, 1000) != PacketReordering(10, 1000)
        assert PacketReordering(50, 1000) != PacketReordering(50, 2000)


class TestPacketCorruption(unittest.TestCase):
    def test_packet_corruption(self):
        qd = PacketCorruption(50)
        assert qd.name == "corrupt"
        assert qd.percent == 50
        assert qd.discipline == "netem corrupt 50%"

    def test_equality(self):
        assert PacketCorruption(50) == PacketCorruption(50)

    def test_inequality(self):
        assert PacketCorruption(50) != PacketCorruption(100)


class TestRateControl(unittest.TestCase):
    def test_rate_control(self):
        qd = RateControl(1, 2, 3)
        assert qd.name == "rate"
        assert qd.kbit == 1
        assert qd.latency_milliseconds == 2
        assert qd.burst_bytes == 3
        assert qd.discipline == "tbf rate 1kbit latency 2ms burst 3"

    def test_equality(self):
        assert RateControl(1, 2, 3) == RateControl(1, 2, 3)

    def test_inequality(self):
        assert RateControl(1, 2, 3) != RateControl(4, 2, 3)
        assert RateControl(1, 2, 3) != RateControl(1, 4, 3)
        assert RateControl(1, 2, 3) != RateControl(1, 2, 4)
