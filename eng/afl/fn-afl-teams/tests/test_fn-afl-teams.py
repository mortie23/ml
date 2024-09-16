import main as fn
import pandas as pd


def test_strip_tags():
    stripped = fn.strip_tags("<span>hello world</span>")
    assert stripped == " hello world "


def test_scrape_data():
    scraped = fn.scrape_data()
    scraped_columns = scraped.columns.tolist()
    scraped_columns == [
        "debut",
        "retirement",
        "abbrev",
        "id",
        "name",
        "logo",
    ]
