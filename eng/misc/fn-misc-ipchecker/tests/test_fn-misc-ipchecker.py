import main as fn


def test_ip_checker():
    ip_address = fn.ip_checker()
    assert type(ip_address) == str
