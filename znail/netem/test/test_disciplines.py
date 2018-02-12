from ..disciplines import PacketCorruption, PacketDelay, PacketDuplication, PacketLoss, \
    PacketReordering, QueueingDiscipline, RateControl


def test_queueing_discipline():
    qd = QueueingDiscipline('name', 'discipline')
    assert qd.name == 'name'
    assert qd.discipline == 'discipline'


def test_packet_delay():
    qd = PacketDelay(1000)
    assert qd.name == 'delay'
    assert qd.milliseconds == 1000
    assert qd.discipline == 'netem delay 1000ms'


def test_packet_loss():
    qd = PacketLoss(50)
    assert qd.name == 'loss'
    assert qd.percent == 50
    assert qd.discipline == 'netem loss 50%'


def test_packet_duplication():
    qd = PacketDuplication(50)
    assert qd.name == 'duplicate'
    assert qd.percent == 50
    assert qd.discipline == 'netem duplicate 50%'


def test_packet_reordering():
    qd = PacketReordering(50, 1000)
    assert qd.name == 'reorder'
    assert qd.percent == 50
    assert qd.milliseconds == 1000
    assert qd.discipline == 'netem delay 1000ms reorder 50%'


def test_packet_corruption():
    qd = PacketCorruption(50)
    assert qd.name == 'corrupt'
    assert qd.percent == 50
    assert qd.discipline == 'netem corrupt 50%'


def test_rate_control():
    qd = RateControl(1, 2, 3)
    assert qd.name == 'rate'
    assert qd.kbit == 1
    assert qd.latency_milliseconds == 2
    assert qd.burst_bytes == 3
    assert qd.discipline == 'tbf rate 1kbit latency 2ms burst 3'
