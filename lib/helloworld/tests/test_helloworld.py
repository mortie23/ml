import helloworld.helloworld as hw


def test_hello():
    hello_message = hw.helloworld('christopher')
    assert hello_message == 'Hello world christopher'
