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
    """
    Funciton that will create poll and insert it into the database
    """
    js = dict()  # creating dictionary for options
    for option in options:  # getting every option
        js[option] = 0  # setting option upvotes to 0
    poll = Poll()  # creating poll orm class
    poll.title = title  # setting up title
    poll.creator = creatorId  # setting up poll creator
    poll.options = str(js)  # setting up poll options
    poll.unique = unique  # setting up poll type
    poll.whoVoted = ''  # setting up poll voters
    db_sess.add(poll)  # adding poll to session
    db_sess.commit()  # commiting changes
    return poll.id  # returning id of created poll


def retreivePoll(db_sess, id):
    """
    Function that return poll by poll id
    """
    poll = db_sess.query(Poll).filter(
        Poll.id == id).first()  # getting poll from database
    return poll  # returning poll itself


def getChartUrl(poll):
    """
    Function that get chart for polls using API

    Args:
        poll (Poll): poll you wanna get chart for

    Returns:
        string: url for chart to created poll
    """
    poll = ast.literal_eval(poll.options)  # getting poll options
    # url = "https://image-charts.com/chart?chco=000000%2C8AC1E7%7C7f3f98%7Cfdb45c&chs=300x300&cht=bvs&chxt=x%2Cy&chd=a%3A10%2C50%2C60%2C80%2C40&chxl=0:|123|321|213|"
    # url = "https://image-charts.com/chart?chco=000000%2C8AC1E7%7C7f3f98%7Cfdb45c&chs=300x300&cht=bvs&chxt=x%2Cy&chd=a%3A0%2C0%2C0&chxl=0:|First clause|Second clause|Third clause|"
    # basic url beginning
    url = "https://image-charts.com/chart?chco=000000%2C8AC1E7%7C7f3f98%7Cfdb45c&chs=500x500&cht=bvs&chxt=x%2Cy&"
    first = True  # need to do this because of wierd api. first element should be 3A
    chd = "chd=a"  # setting up chd
    chxl = "chxl=0:|"  # setting up chxl
    for key, value in poll.items():  # cycle with all options
        chxl += key.replace(" ", "_") + "|"  # adding option to url
        if first:  # special first option
            first = False  # making first not first
            chd += "%" + "3A" + str(value)  # adding option to chd
        else:  # if not first
            chd += "%" + "2C" + str(value)  # adding option to chd
    url += chd + "&" + chxl  # creating whole url
    return url  # returning url


def getPollJson(db_sess, id):
    """
    Function that will return poll as dictionary by poll id

    Args:
        db_sess (Session): current database session
        id (int): id of provided poll

    Returns:
        dict: polls options
    """
    poll = retreivePoll(db_sess, id)  # getting poll from database
    """setting up poll """
    if poll is None:
        return None
    return {
        'title': poll.title,
        'options': ast.literal_eval(poll.options),
        'isUnique': poll.unique,
        'whoVoted': list(map(int, poll.whoVoted.split())),
        'chart_url': getChartUrl(poll)
    }


def voteInPoll(db_sess, pollId, uid, answer_options):
    """
    Function that votes in poll when user votes on website

    Args:
        db_sess (Session): current database session
        pollId (int): id of poll that user voted in
        uid (int): id of user who voted in poll
        answer_options (list): options that user has chosen from poll
    """
    poll = retreivePoll(db_sess, pollId)  # getting poll
    votesList = poll.whoVoted  # getting string of users who voted in poll
    votesList = votesList.split()  # converting string to list
    votesList.append(uid)  # appending user to list
    # converting list to string
    votesList = ' '.join(list(map(str, votesList)))
    options = ast.literal_eval(poll.options)  # getting all options
    for option in answer_options:  # cycle of all options that user has chosen
        # try except if user edited html form
        try:
            options[option] += 1  # adding vote
        except KeyError:
            pass
    poll.options = str(options)  # setting up new votes
    poll.whoVoted = votesList  # setting up new users who voted list
    db_sess.commit()  # comminting changes
