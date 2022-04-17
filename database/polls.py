from .db_session import SqlAlchemyBase
import sqlalchemy
import ast


class Poll(SqlAlchemyBase):
    """orm poll model"""
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

def getChartUrl(poll):
    poll = ast.literal_eval(poll.options)
    # url = "https://image-charts.com/chart?chco=000000%2C8AC1E7%7C7f3f98%7Cfdb45c&chs=300x300&cht=bvs&chxt=x%2Cy&chd=a%3A10%2C50%2C60%2C80%2C40&chxl=0:|123|321|213|"
    # url = "https://image-charts.com/chart?chco=000000%2C8AC1E7%7C7f3f98%7Cfdb45c&chs=300x300&cht=bvs&chxt=x%2Cy&chd=a%3A0%2C0%2C0&chxl=0:|First clause|Second clause|Third clause|"
    url = "https://image-charts.com/chart?chco=000000%2C8AC1E7%7C7f3f98%7Cfdb45c&chs=500x500&cht=bvs&chxt=x%2Cy&"
    first = True
    chd = "chd=a"
    chxl = "chxl=0:|"
    for key, value in poll.items():
        chxl += key.replace(" ", "_") + "|"
        if first:
            first = not first
            chd += "%" + "3A" + str(value)
        else:
            chd += "%" + "2C" + str(value)
    url += chd + "&" + chxl
    return url
    
    

def getPollJson(db_sess, id):
    poll = retreivePoll(db_sess, id)
    return {
        'title': poll.title,
        'options': ast.literal_eval(poll.options),
        'isUnique': poll.unique,
        'whoVoted': list(map(int, poll.whoVoted.split())),
        'chart_url': getChartUrl(poll)
    }
    
    
def voteInPoll(db_sess, pollId, uid, answer_options):
    poll = retreivePoll(db_sess, pollId)
    votesList = poll.whoVoted
    votesList = votesList.split()
    votesList.append(uid)
    votesList = ' '.join(list(map(str, votesList)))
    options = ast.literal_eval(poll.options)
    for option in answer_options:
        options[option] += 1
    poll.options = str(options)
    poll.whoVoted = votesList
    db_sess.commit()
    