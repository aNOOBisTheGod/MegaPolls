from flask import Flask, render_template, request, make_response, redirect, url_for, flash  # flask modules
from database.polls import createPoll, getPollJson, voteInPoll  # database file
from utils.exceptions import *  # custom exceptions
from database import db_session  # database
import database.users  # database file
import logging  # for logs
import sys  # for logs

app = Flask(__name__)  # creating application
app.config['SESSION_TYPE'] = 'filesystem'  # setting up session_type
# setting up very secret key
app.secret_key = 'you wont hack this website cause youre stupid'
db_session.global_init("db/data.db")  # initializing database
# notice, that you should push to heroku with database
# because heroku don't allow user to create files
db_sess = db_session.create_session()  # creating database session


@app.route('/', methods=['POST', 'GET'])
def mainpage():
    """this function simply renders main page which html code stores in index.html"""
    isFirstTime = request.cookies.get(
        'firstTime')  # checkin' if user visiting website first time
    if isFirstTime is None:  # if user visiting website first time
        # info about cookie policy
        flash(
            "If you will use this website then you accept the cookies we provide.", "info")
        resp = make_response(render_template('index.html')
                             )  # making responce for cookie
        resp.set_cookie('firstTime', '1')  # setting cookie
        return resp  # returning responce with cookie
    # flash(f"Heroku deployment test", "success")
    return render_template('index.html')  # rendering remplate for main page


@app.route('/account', methods=['POST', 'GET'])
def accountpage():
    """
    this function returns page where you can see your usename and you can log out your account
    logging out happens when you click "log out" button in form, which creates POST method.
    then application redirects you to create account page and sets password and email cookies to nothing
    if user isn't logged in accound, application will redirect him to create account page
    """
    username = request.cookies.get('username')  # getting user password
    password = request.cookies.get('password')  # gettings user email adress
    if request.method == "POST":  # triggers when user press the button
        # getting template for create account page
        resp = make_response(redirect(url_for('createaccountpage')))
        resp.set_cookie('username', '0')  # reseting username
        resp.set_cookie('password', '0')  # reseting password
        return resp  # returning create account page
    # check if user is in database using username and password
    if database.users.checkUser(username, password):
        # renders account page template(account.html)
        return render_template('account.html', username=username)
    else:  # if user is not in database
        # redirecting to create account page
        return redirect(url_for(('createaccountpage')))


@app.route('/create_account', methods=['POST', 'GET'])
def createaccountpage():
    """
    This route helps user to create account or log in it
    """
    username = request.cookies.get(
        'username')  # getting username using cookies
    # getting password using cookies
    password = request.cookies.get('password')
    # checking if user is logged in
    if database.users.checkUser(username, password):
        # if user is logged in, then redirecting to account page
        return redirect(url_for('accountpage'))
    if request.method == "POST":  # triggers when user press "create account" or "log in" buttons
        try:  # try except usage to show user his mistakes using sweetalert2 JS library
            if "create_account" in request.form:  # check if user creates new account
                # getting password from form
                password = request.form['password']
                # getting username from form
                username = request.form['username']
                if database.users.checkUser(username, password):
                    raise UserException(
                        "This user already exist. Use log in form to log in account.")
                # checking if username or password are long enough
                if len(username) < 6 or len(password) < 6:
                    # raising exception to show user what to do
                    raise Exception(
                        'Length of username and pass must be longer than 5 symbols')
                user = database.users.User()  # creating new user instacne
                user.username = username  # setting username
                user.password = password  # setting password
                # settings list of polls that user created, maybe will be released later
                user.pollsCreated = ''
                db_sess.add(user)  # adding user to database
                db_sess.commit()  # commiting database changes
                # getting template for account route
                resp = make_response(redirect(url_for('accountpage')))
                """setting up cookies to log in user automatically"""
                resp.set_cookie('username', username)  # username cookie
                resp.set_cookie('password', password)  # password cookie
                return resp  # returning created account route template
            else:  # if user loggs in account
                # getting username from form
                username = request.form['username_login']
                # getting password from form
                password = request.form['password_login']
                # check if user exists
                if database.users.checkUser(username, password):
                    # getting template for account page
                    resp = make_response(redirect(url_for('accountpage')))
                    """setting up cookies to log in user automatically"""
                    resp.set_cookie('username', username)  # username cookie
                    resp.set_cookie('password', password)  # password cookie
                    return resp  # returning create account route template
                else:  # if user not exists
                    # show information to user
                    raise UserException(
                        'User not found! Make sure username and password are correct')
        except Exception as e:  # gettings exception error code
            flash(f"{e}", "error")  # creating alert
            # returning same template
            return render_template('create_account.html')

    return render_template('create_account.html')


@app.route('/poll', methods=['POST', 'GET'])
def pollpage():
    """
    function that returns polls route(poll.html)
    if user already voted in poll, he will be notified and will be able to see results
    if not, he will be able to vote
    or else, if user isn't logged in, function will redirect him to create account page
    """
    lockPoll = False  # setting up poll lock flag
    password = request.cookies.get('password')  # getting password from cookies
    username = request.cookies.get('username')  # getting username from cookies
    # checking if user exists
    if not database.users.checkUser(username, password):
        # if not, returns create account page
        return redirect(url_for('createaccountpage'))
    pollId = request.args.get('poll')  # getting poll id from args line
    # getting poll in JSON format to pass to HTML
    poll = getPollJson(db_sess, pollId)
    if poll is None:
        flash('Poll does not exist!', 'error')
        return render_template('index.html')
    # checking if user has already voted
    if database.users.getUserId(username, password) in poll['whoVoted']:
        lockPoll = True  # if yes, then poll will be locked for this user
    if request.method == "POST":  # triggers when user votes in poll
        answers = request.form.getlist('answer')  # getting user answers
        # checking if user didn't cheat
        if poll['isUnique'] and len(answers) > 1:
            flash('Do not try to cheat, little html hacker',
                  'error')  # tell user that he's bad
            # renders poll.html template with current poll
            return render_template('poll.html', poll=poll, isLocked=lockPoll)
        # function that will write user answers to database
        voteInPoll(db_sess, pollId, database.users.getUserId(
            username, password), answers)
        # creating alert that user is good guy
        flash(f"Thanks for voting!", "success")
        return redirect(url_for('mainpage'))  # return user to main page
    # rendering template will poll that we've fetched
    return render_template('poll.html', poll=poll, isLocked=lockPoll)


@app.route('/create_poll', methods=['POST', 'GET'])
def createpollpage():
    """
    this function returns page where user can create poll
    """
    if request.method == "POST":  # triggers when user press "create" button
        try:  # try except to send error messages to user
            unique = False if request.form.get(
                'isUnique') is None else True  # checking if poll is unique
            title = request.form.get('title')  # getting poll title
            # getting list of all clauses
            clauses = request.form.getlist('clause')
            username = request.cookies.get('username')  # getting user username
            password = request.cookies.get('password')  # getting user password
            # checking if user exists
            if database.users.checkUser(username, password):
                pollId = createPoll(db_sess, title, database.users.getUserId(
                    username, password), unique, clauses)  # if yes, creating poll
                # updates user: adds poll to user.pollsCreated
                database.users.updateUser(username, password, pollId)
                # notifying user that poll was created and giving instructions, how to share it
                flash(
                    'Poll created! To share poll, just copy this page link.', 'success')
                # redirecting user to polls route
                return redirect(url_for('pollpage', poll=pollId))
            else:  # if user is not in database
                # creating error alert message
                raise UserException(
                    'User not found, log in account or create a new one')
        except UserException as e:  # if we receive user exception
            flash(f"{e}", "error")  # creating alert itself
            # redirecting to create account route
            return redirect(url_for(('createaccountpage')))
    # returns create_poll.html template
    return render_template('create_poll.html')


if __name__ == "__main__":  # here porgram starts
    """here is the start of the program"""
    app.logger.addHandler(logging.StreamHandler(
        sys.stdout))  # heroku logs addition
    app.logger.setLevel(logging.ERROR)  # heroku loggs addition
    app.run(debug=True, port=5000, host='0.0.0.0')
