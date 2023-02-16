import sayhello.hello as sh


def test_hello():
    hello_message = sh.hello('christopher')
    assert hello_message == 'Hello christopher'
