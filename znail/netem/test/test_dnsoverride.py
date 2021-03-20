from ..dnsoverride import DnsOverrideDescriptor


def test_dns_override_descriptor():
    d = DnsOverrideDescriptor("hostname", "1.2.3.4")
    assert d.hostname == "hostname"
    assert d.ip_address == "1.2.3.4"
    assert str(d) == "DNS override hostname -> 1.2.3.4"


def test_dns_override_descriptor_with_no_ip_address():
    d = DnsOverrideDescriptor("hostname")
    assert d.hostname == "hostname"
    assert d.ip_address is None
    assert str(d) == "DNS override hostname -> (nothing)"


def test_dns_override_descriptor_is_hashable():
    a = DnsOverrideDescriptor("hostname", "1.2.3.4")
    b = DnsOverrideDescriptor("hostname", "1.2.3.4")
    c = DnsOverrideDescriptor("hostname", "4.3.2.1")
    d = DnsOverrideDescriptor("hostname")
    assert hash(a) == hash(b)
    assert hash(a) != hash(c)
    assert hash(a) != hash(d)
    assert hash(d) == hash(d)


def test_dns_override_descriptor_has_equality_operator():
    a = DnsOverrideDescriptor("hostname", "1.2.3.4")
    b = DnsOverrideDescriptor("hostname", "1.2.3.4")
    c = DnsOverrideDescriptor("hostname", "4.3.2.1")
    d = DnsOverrideDescriptor("hostname")
    assert a == b
    assert a != c
    assert a != d
    assert d == d


def test_dns_override_descriptor_is_less_than_comparable():
    a = DnsOverrideDescriptor("a", "1.2.3.4")
    b = DnsOverrideDescriptor("b", "1.2.3.4")
    c = DnsOverrideDescriptor("b", "2.3.4.5")
    d = DnsOverrideDescriptor("b", "0.0.0.0")
    assert a < b
    assert b < c
    assert d < b
