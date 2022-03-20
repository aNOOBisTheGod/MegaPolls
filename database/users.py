from enum import unique
import sqlalchemy
import sqlite3
from utils.exceptions import UserException

from .db_session import SqlAlchemyBase


class User(SqlAlchemyBase):
    __tablename__ = 'users'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    username = sqlalchemy.Column(sqlalchemy.String, nullable=True, unique=True)
    password = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    pollsCreated = sqlalchemy.Column(sqlalchemy.String, nullable=True)


def checkUser(username, password):
    try:
        connection = sqlite3.connect('db/data.db')
        cursor = connection.cursor()
        query = f"""SELECT * FROM USERS WHERE username = '{username}' AND password = '{password}' """
        res = cursor.execute(query).fetchone()
    except Exception as e:
        print(e)
        return False
    if res != None:
        return True
    else:
        return False
    

def getUserId(username, password):
    connection = sqlite3.connect('db/data.db')
    cursor = connection.cursor()
    query = f"""SELECT id FROM USERS WHERE username = '{username}' AND password = '{password}'"""
    res = cursor.execute(query).fetchone()
    if res != None:
        return res[0]
    else:
        raise UserException('404 user not found')
    
def updateUser(username, password, newPoll):
    connection = sqlite3.connect('db/data.db')
    cursor = connection.cursor()    
    query = f"""SELECT pollsCreated FROM USERS WHERE username = '{username}' AND password = '{password}'"""
    res = cursor.execute(query).fetchone()
    print(res)
    polls = res[0].split()
    print(polls)
    polls.append(newPoll)
    print(polls)
    polls = ' '.join(list(map(str, polls)))
    print(polls)
    query = f"""UPDATE USERS SET pollsCreated = "{polls}" WHERE password = '{password}' AND username = '{username}'"""
    cursor.execute(query)
    connection.commit()
