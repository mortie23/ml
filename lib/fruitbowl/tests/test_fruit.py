import fruitbowl.fruit as fr

"""
Usage: 
    # Run all unit tests
    poetry run pytest
    # Run a single unit test
    poetry run pytest tests\test_fruit.py::test_get_fruit
"""


def test_get_fruit():
    random_fruit = fr.get_fruit()
    assert random_fruit in [
        "Watermelon",
        "Strawberry",
        "Pineapple",
        "Papaya",
        "Orange",
        "Mango",
        "Kiwi",
        "Blueberry",
        "Banana",
        "Apple",
        "Currant",
        "Fig",
        "Gooseberry",
        "Date",
        "Olive",
        "Tangerine",
        "Apricot",
    ]
