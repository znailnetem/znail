def test_startup_procedure(Znail):
    with Znail() as znail:
        pass
    assert "-t nat -F" in znail.stdout
    assert "-t nat -A POSTROUTING -o eth0 -j MASQUERADE" in znail.stdout
    assert "qdisc del dev eth1 root" in znail.stdout
