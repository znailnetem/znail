"""
Interact with the "tc" command line utility.

For more information about "tc", please see:
http://man7.org/linux/man-pages/man8/tc.8.html
"""
import functools

from .util import run_in_shell, tc


class Tc:
    def __init__(self, adapter):
        self._adapter = adapter
        self._queueing_disciplines = {}
        self._whitelist = []
        self.clear()

    @classmethod
    @functools.lru_cache()
    def adapter(cls, adapter):
        return cls(adapter)

    def apply(self, disciplines):
        self.clear()
        self._queueing_disciplines = disciplines
        self._setup_queueing_disciplines()
        self._setup_whitelist()

    @property
    def disciplines(self):
        return self._queueing_disciplines

    @property
    def whitelist(self):
        return self._whitelist

    @whitelist.setter
    def whitelist(self, value):
        self._whitelist = value

    def clear(self):
        # When deleted, the root qdisc is automatically replaced with the default.
        run_in_shell("{tc} qdisc del dev {adapter} root || true".format(tc=tc, adapter=self._adapter))

    def _setup_queueing_disciplines(self):
        # If there is nothing to be done, stick with the default queueing discipline.
        if not self._queueing_disciplines:
            return

        # Sets up a root queue that sends all traffic to the impairment queue.
        run_in_shell(
            "{tc} qdisc add dev {adapter} root "
            "handle 1: prio bands 2 "
            "priomap 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1".format(tc=tc, adapter=self._adapter)
        )

        # Sets up a queue where we can send traffic that is not to be impaired.
        run_in_shell("{tc} qdisc add dev {adapter} parent 1:1 " "handle 10: pfifo".format(tc=tc, adapter=self._adapter))

        # Sets up the impairment queue.
        disciplines = list(self._queueing_disciplines.values())
        run_in_shell(
            "{tc} qdisc add dev {adapter} parent 1:2 "
            "handle 20: {discipline}".format(tc=tc, adapter=self._adapter, discipline=disciplines[0].discipline)
        )
        for parent_handle, discipline in enumerate(disciplines[1:], start=20):
            run_in_shell(
                "{tc} qdisc add dev {adapter} parent "
                "{parent_handle}: handle {handle}: {discipline}".format(
                    tc=tc,
                    adapter=self._adapter,
                    parent_handle=parent_handle,
                    handle=parent_handle + 1,
                    discipline=discipline.discipline,
                )
            )

    def _setup_whitelist(self):
        # If there is nothing to be done, stick with the default queueing discipline.
        if not self._queueing_disciplines:
            return

        for ip in self._whitelist:
            run_in_shell(
                "{tc} filter add dev {adapter} parent 1: "
                "protocol ip prio 1 u32 "
                "match ip dst {ip}/32 flowid 1:1".format(tc=tc, adapter=self._adapter, ip=ip)
            )
            run_in_shell(
                "{tc} filter add dev {adapter} parent 1: "
                "protocol ip prio 1 u32 "
                "match ip src {ip}/32 flowid 1:1".format(tc=tc, adapter=self._adapter, ip=ip)
            )
