from ..ipredirect import IpRedirectDescriptor


def test_ip_redirect_descriptor():
    d = IpRedirectDescriptor("1.2.3.4", 1, "4.3.2.1", 2, "tcp")
    assert d.iptables_commandline == "-d 1.2.3.4 -p tcp --dport 1 -j DNAT --to-destination 4.3.2.1:2"
    assert str(d) == "IP redirect 1.2.3.4:1 -> 4.3.2.1:2 (tcp)"


def test_ip_redirect_descriptor_is_hashable():
    a = IpRedirectDescriptor("1.2.3.4", 1, "4.3.2.1", 2, "tcp")
    b = IpRedirectDescriptor("1.2.3.4", 1, "4.3.2.1", 2, "tcp")
    c = IpRedirectDescriptor("4.3.2.1", 3, "1.2.3.4", 1, "tcp")
    assert hash(a) == hash(b)
    assert hash(a) != hash(c)


def test_ip_redirect_descriptor_has_equality_operator():
    a = IpRedirectDescriptor("1.2.3.4", 1, "4.3.2.1", 2, "tcp")
    b = IpRedirectDescriptor("1.2.3.4", 1, "4.3.2.1", 2, "tcp")
    c = IpRedirectDescriptor("4.3.2.1", 3, "1.2.3.4", 1, "tcp")
    assert a == b
    assert a != c


def test_ip_redirect_descriptor_is_less_than_comparable():
    a = IpRedirectDescriptor("1.2.3.4", 1, "2.3.4.5", 2, "tcp")
    b = IpRedirectDescriptor("2.2.3.4", 1, "2.3.4.5", 2, "tcp")
    c = IpRedirectDescriptor("2.2.3.4", 2, "2.3.4.5", 2, "tcp")
    d = IpRedirectDescriptor("2.2.3.4", 2, "3.3.4.5", 2, "tcp")
    e = IpRedirectDescriptor("2.2.3.4", 2, "3.3.4.5", 3, "tcp")
    f = IpRedirectDescriptor("2.2.3.4", 2, "3.3.4.5", 3, "udp")
    assert a < b
    assert b < c
    assert c < d
    assert d < e
    assert e < f
