from firebase_admin import firestore
from .db_session import SqlAlchemyBase
import sqlalchemy
from database import db_session
import ast
import sqlalchemy.orm as orm
from database.users import User
from sqlalchemy import update


class Poll(SqlAlchemyBase):
    __tablename__ = "polls"
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    creator = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    unique = sqlalchemy.Column(sqlalchemy.Boolean, nullable=True)
    whoVoted = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    options = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    
def createPoll(db_sess, title, creatorId, unique, options):
    js = dict()
    for option in options:
        js[option] = 0
    poll = Poll()
    poll.title = title
    poll.creator = creatorId
    poll.options = str(js)
    poll.unique = unique
    poll.whoVoted = ''
    db_sess.add(poll)
    db_sess.commit()
    return poll.id
    
def retreivePoll(db_sess, id):
    poll = db_sess.query(Poll).filter(Poll.id == id).first()
    return poll

def getPollJson(db_sess, id):
    poll = retreivePoll(db_sess, id)
    return {
        'title': poll.title,
        'options': ast.literal_eval(poll.options),
        'isUnique': poll.unique,
        'whoVoted': list(map(int, poll.whoVoted.split()))
    }
    
    
def voteInPoll(db_sess, pollId, uid, options):
    poll = retreivePoll(db_sess, pollId)
    votesList = poll.whoVoted
    votesList = votesList.split()
    votesList.append(uid)
    print(votesList)
    votesList = ' '.join(list(map(str, votesList)))
    options = ast.literal_eval(poll.options)
    for option in options:
        options[option] += 1
    poll.options = str(options)
    poll.whoVoted = votesList
    db_sess.commit()
    
    

    