import streamlit as st
import sqlite3
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_PATH = os.getenv("DATABASE_PATH")


def create_task(task):
    with sqlite3.connect(DATABASE_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO tasks (task) VALUES (?)", (task,))
        conn.commit()


def read_tasks():
    with sqlite3.connect(DATABASE_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tasks")
        return cursor.fetchall()


def update_task(task_id, new_task):
    with sqlite3.connect(DATABASE_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE tasks SET task = ? WHERE id = ?", (new_task, task_id))
        conn.commit()


def delete_task(task_id):
    with sqlite3.connect(DATABASE_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        conn.commit()


def show_home_page():
    st.title("To-Do Application")

    task = st.text_input("Enter a new task")
    if st.button("Add Task"):
        create_task(task)
        st.success("Task added!")

    tasks = read_tasks()
    if tasks:
        st.write("### Current Tasks")
        for task in tasks:
            task_id, task_name = task
            col1, col2 = st.columns(2)
            with col1:
                st.write(task_name)
            with col2:
                if st.button(f"Update {task_name}"):
                    new_task = st.text_input("Update task", value=task_name)
                    if st.button("Submit Update"):
                        update_task(task_id, new_task)
                        st.success("Task updated!")
                if st.button(f"Delete {task_name}"):
                    delete_task(task_id)
                    st.success("Task deleted!")
    else:
        st.write("No tasks available.")
