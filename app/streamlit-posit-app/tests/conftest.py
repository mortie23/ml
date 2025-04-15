import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.model import Base, Task  # Updated import path
from dotenv import load_dotenv
import os


@pytest.fixture
def test_database_url():
    """Create a test database in memory"""
    load_dotenv()
    TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")

    yield TEST_DATABASE_URL
