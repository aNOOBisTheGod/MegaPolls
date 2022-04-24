from enum import unique
import sqlalchemy
import sqlite3
from utils.exceptions import UserException

from .db_session import SqlAlchemyBase


class User(SqlAlchemyBase):
    """orm user model"""
    __tablename__ = 'users'  # table where data will be stored
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)  # primary key
    username = sqlalchemy.Column(
        sqlalchemy.String, nullable=True, unique=True)  # username
    password = sqlalchemy.Column(sqlalchemy.String, nullable=True)  # password
    pollsCreated = sqlalchemy.Column(
        sqlalchemy.String, nullable=True)  # list of created polls


def checkUser(username, password):
    """function that will check if user exists"""
    try:  # user exists
        connection = sqlite3.connect('db/data.db')  # connecting to database
        cursor = connection.cursor()  # connection cursor creation
        query = f"""SELECT * FROM USERS WHERE username = '{username}' AND password = '{password}' """  # SQL query to execute
        res = cursor.execute(query).fetchone()  # result of query
    except Exception as e:  # user doesn't exist
        return False  # return false cause user doesn't exist
    if res != None:  # if there are no users with such a data
        return True  # return true cause user exists
    else:  # that mean that result is None so user not found in database
        return False  # return false cause user doesn't exist


def getUserId(username, password):
    """this function returns user id by username and password"""
    connection = sqlite3.connect('db/data.db')  # conneting to database
    cursor = connection.cursor()  # creating connection cursor
    query = f"""SELECT id FROM USERS WHERE username = '{username}' AND password = '{password}'"""  # SQL query to execute
    res = cursor.execute(query).fetchone()  # fetching data
    if res != None:  # user found
        return res[0]  # return id
    else:  # user not found
        raise UserException('404 user not found')  # raising exception


def updateUser(username, password, newPoll):
    """
    Function that updates user when he creates poll
    """
    connection = sqlite3.connect('db/data.db')  # connecting to database
    cursor = connection.cursor()  # creating connection cursor
    query = f"""SELECT pollsCreated FROM USERS WHERE username = '{username}' AND password = '{password}'"""  # making SQL query
    res = cursor.execute(query).fetchone()  # executing query
    polls = res[0].split()  # converting string of polls to list
    polls.append(newPoll)  # appending new poll to polls list
    polls = ' '.join(list(map(str, polls)))  # converting polls list to string
    query = f"""UPDATE USERS SET pollsCreated = "{polls}" WHERE password = '{password}' AND username = '{username}'"""  # making SQL query to update db
    cursor.execute(query)  # executing query
    connection.commit()  # commiting changes
