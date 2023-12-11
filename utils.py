from db import *
from sqlalchemy import insert, select


# this function for saving task to Tasks table
def task_save(title: str, desc: str, from_user: int):
    query = insert(Tasks).values(title=title, description=desc, user_id=from_user)
    session.execute(query)
    session.commit()


# this function to gather tasks for user
def get_user_tasks(from_user: int):
    select_query = select(Tasks.title, Tasks.description).where(Tasks.user_id == from_user)
    results = session.execute(select_query).all()
    if results:
        return results
    else:
        return None
