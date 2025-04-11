from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.model import Task, Base


def get_db_session(database_url):
    engine = create_engine(database_url)
    Session = sessionmaker(bind=engine)
    return Session()


def create_task(task_text, database_url):
    session = get_db_session(database_url)
    new_task = Task(task=task_text)
    session.add(new_task)
    session.commit()
    session.close()


def read_tasks(database_url):
    session = get_db_session(database_url)
    tasks = session.query(Task).all()
    result = [(task.id, task.task) for task in tasks]
    session.close()
    return result


def update_task(task_id, new_task_text, database_url):
    session = get_db_session(database_url)
    task = session.query(Task).filter(Task.id == task_id).first()
    if task:
        task.task = new_task_text
        session.commit()
    session.close()


def delete_task(task_id, database_url):
    session = get_db_session(database_url)
    task = session.query(Task).filter(Task.id == task_id).first()
    if task:
        session.delete(task)
        session.commit()
    session.close()
