"""
Queueing disciplines (qdisc in tc terminology) describes the flow of packets.

For more information about "tc" queueing disciplines, please see:
http://man7.org/linux/man-pages/man8/tc.8.html
"""


class QueueingDiscipline:
    """Base class for all queueing disciplines."""

    def __init__(self, name, discipline):
        self._name = name
        self._discipline = discipline

    @property
    def name(self):
        return self._name

    @property
    def discipline(self):
        return self._discipline

    def __eq__(self, other):
        for k, v in self.__dict__.items():
            if not k.startswith("__"):
                if v != other.__dict__[k]:
                    return False
        return True


class PacketDelay(QueueingDiscipline):
    """Queueing discipline that adds fixed delay to all packets."""

    def __init__(self, milliseconds):
        self._milliseconds = milliseconds
        super().__init__("delay", "netem delay {milliseconds}ms".format(milliseconds=milliseconds))

    @property
    def milliseconds(self):
        return self._milliseconds


class PacketLoss(QueueingDiscipline):
    """Queueing discipline that drop a percentage of all packets."""

    def __init__(self, percent):
        self._percent = percent
        super().__init__("loss", "netem loss {percent}%".format(percent=percent))

    @property
    def percent(self):
        return self._percent


class PacketDuplication(QueueingDiscipline):
    """Queueing discipline that transmits a percentage of all packets twice."""

    def __init__(self, percent):
        self._percent = percent
        super().__init__("duplicate", "netem duplicate {percent}%".format(percent=percent))

    @property
    def percent(self):
        return self._percent


class PacketReordering(QueueingDiscipline):
    """
    Queueing discipline that reorders packets.

    Packets are reordered by sending a percentage of all packets immediately while delaying others.
    """

    def __init__(self, percent, milliseconds):
        self._percent = percent
        self._milliseconds = milliseconds
        super().__init__(
            "reorder",
            "netem delay {milliseconds}ms reorder {percent}%".format(milliseconds=milliseconds, percent=percent),
        )

    @property
    def percent(self):
        return self._percent

    @property
    def milliseconds(self):
        return self._milliseconds


class PacketCorruption(QueueingDiscipline):
    """
    Queueing discipline that Corrupts a percent of all packets.

    Packets are corrupted by introducing single bit errors.
    """

    def __init__(self, percent):
        self._percent = percent
        super().__init__("corrupt", "netem corrupt {percent}%".format(percent=percent))

    @property
    def percent(self):
        return self._percent


class RateControl(QueueingDiscipline):
    """Queueing disciline that controls the rate at which packets are transmitted."""

    def __init__(self, kbit, latency_milliseconds, burst_bytes):
        self._kbit = kbit
        self._latency_milliseconds = latency_milliseconds
        self._burst_bytes = burst_bytes
        super().__init__(
            "rate",
            "tbf rate {kbit}kbit latency {latency_milliseconds}ms burst {burst_bytes}".format(
                kbit=kbit, latency_milliseconds=latency_milliseconds, burst_bytes=burst_bytes
            ),
        )

    @property
    def kbit(self):
        return self._kbit

    @property
    def latency_milliseconds(self):
        return self._latency_milliseconds

    @property
    def burst_bytes(self):
        return self._burst_bytes
