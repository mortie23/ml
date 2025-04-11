import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.model import Base, Task  # Updated import path


@pytest.fixture
def test_db():
    """Create a test database in memory"""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    # Add some test data
    test_tasks = [
        Task(task="Test task 1"),
        Task(task="Test task 2"),
        Task(task="Test task 3"),
    ]
    session.add_all(test_tasks)
    session.commit()

    yield "sqlite:///:memory:"

    Base.metadata.drop_all(engine)
