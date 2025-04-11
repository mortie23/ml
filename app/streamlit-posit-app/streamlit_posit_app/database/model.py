from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    task = Column(String(200), nullable=False)

    def __repr__(self):
        return f"<Task(id={self.id}, task='{self.task}')>"


# Create database engine and tables
def init_db(database_url):
    engine = create_engine(database_url)
    Base.metadata.create_all(engine)
