from flask import Flask, render_template, request, make_response, redirect, url_for, flash
from database.polls import createPoll, getPollJson, voteInPoll
from utils.exceptions import *
from database import db_session
import database.users
import logging
import sys
import os

app = Flask(__name__) #creating application
app.config['SESSION_TYPE'] = 'filesystem' #setting up session_type
app.secret_key = 'you wont hack this website cause youre stupid' #setting up very secret key
db_session.global_init("db/data.db") #initializing database
#notice, that you should push to heroku with database
#because heroku don't allow user to create files
db_sess = db_session.create_session() #creating database session

@app.route('/', methods=['POST', 'GET'])
def mainpage():
    """this function simply renders main page which html code stores in index.html"""
    flash(f"Heroku deployment test", "success")
    return render_template('index.html')

@app.route('/account', methods=['POST', 'GET'])
def accountpage():
    """
    this function returns page where you can see your usename and you can log out your account
    logging out happens when you click "log out" button in form, which creates POST method.
    then application redirects you to create account page and sets password and email cookies to nothing
    if user isn't logged in accound, application will redirect him to create account page
    """
    username = request.cookies.get('username') #getting user password
    password = request.cookies.get('password') #gettings user email adress
    if request.method == "POST": #triggers when user press the button
        resp = make_response(redirect(url_for('createaccountpage'))) #getting template for create account page
        resp.set_cookie('username', '0') #reseting username
        resp.set_cookie('password', '0') #reseting password
        return resp #returning create account page
    if database.users.checkUser(username, password): #check if user is in database using username and password
        return render_template('account.html', username=username) #renders account page template(account.html)
    else: #if user is not in database
        return redirect(url_for(('createaccountpage'))) #redirecting to create account page

@app.route('/create_account', methods=['POST', 'GET'])
def createaccountpage():
    """
    This route helps user to create account or log in it
    """
    username = request.cookies.get('username') #getting username using cookies
    password = request.cookies.get('password') #getting password using cookies
    if database.users.checkUser(username, password): #checking if user is logged in
        return redirect(url_for('accountpage')) #if user is logged in, then redirecting to account page
    if request.method == "POST": #triggers when user press "create account" or "log in" buttons
        try: #try except usage to show user his mistakes using sweetalert2 JS library
            if "create_account" in request.form: #check if user creates new account
                password = request.form['password'] #getting password from form
                username = request.form['username'] #getting username from form
                if len(username) < 6 or len(password) < 6: #checking if username or password are long enough
                    raise Exception('Length of username and pass must be longer than 5 symbols') #raising exception to show user what to do
                user = database.users.User() #creating new user instacne
                user.username = username #setting username
                user.password = password #setting password
                user.pollsCreated = '' #settings list of polls that user created, maybe will be released later
                db_sess.add(user) #adding user to database
                db_sess.commit() #commiting database changes
                resp = make_response(redirect(url_for('accountpage'))) #getting template for account route
                """setting up cookies to log in user automatically"""
                resp.set_cookie('username', username) #username cookie
                resp.set_cookie('password', password) #password cookie
                return resp #returning created account route template
            else: # if user loggs in account
                username = request.form['username_login'] #getting username from form
                password = request.form['password_login'] #getting password from form
                if database.users.checkUser(username, password): #check if user exists
                    resp = make_response(redirect(url_for('accountpage'))) #getting template for account page
                    """setting up cookies to log in user automatically"""
                    resp.set_cookie('username', username) #username cookie
                    resp.set_cookie('password', password) #password cookie
                    return resp #returning create account route template
                else: #if user not exists
                    raise UserException('User not found! Make sure username and password are correct') #show information to user
        except Exception as e: #gettings exception error code
            flash(f"{e}", "error") #creating alert
            return render_template('create_account.html') #returning same template

    return render_template('create_account.html')

@app.route('/poll', methods=['POST', 'GET'])
def pollpage():
    """
    function that returns polls route(poll.html)
    if user already voted in poll, he will be notified and will be able to see results
    if not, he will be able to vote
    or else, if user isn't logged in, function will redirect him to create account page
    """
    lockPoll = False #setting up poll lock flag
    password = request.cookies.get('password') #getting password from cookies
    username = request.cookies.get('username') #getting username from cookies
    if not database.users.checkUser(username, password): #checking if user exists
        return redirect(url_for('createaccountpage')) #if not, returns create account page
    pollId = request.args.get('poll') #getting poll id from args line
    poll = getPollJson(db_sess, pollId) #getting poll in JSON format to pass to HTML
    if database.users.getUserId(username, password) in poll['whoVoted']: #checking if user has already voted 
        lockPoll = True #if yes, then poll will be locked for this user
    if request.method == "POST": #triggers when user votes in poll
        answers = request.form.getlist('answer') #getting user answers
        if poll['isUnique'] and len(answers) > 1: #checking if user didn't cheat
            flash('Do not try to cheat, little html hacker', 'error') #tell user that he's bad
            return render_template('poll.html', poll=poll, isLocked=lockPoll) #renders poll.html template with current poll
        voteInPoll(db_sess, pollId, database.users.getUserId(username, password), answers) #function that will write user answers to database
        flash(f"Thanks for voting!", "success") #creating alert that user is good guy
        return redirect(url_for('mainpage')) #return user to main page
    return render_template('poll.html', poll=poll, isLocked=lockPoll) #rendering template will poll that we've fetched

@app.route('/create_poll', methods=['POST', 'GET'])
def createpollpage():
    """
    this function returns page where user can create poll
    """
    if request.method == "POST": #triggers when user press "create" button
        try: #try except to send error messages to user
            unique = False if request.form.get('isUnique') is None else True #checking if poll is unique
            title = request.form.get('title') #getting poll title
            clauses=request.form.getlist('clause') #getting list of all clauses
            username = request.cookies.get('username') #getting user username
            password = request.cookies.get('password') #getting user password
            if database.users.checkUser(username, password): #checking if user exists
                pollId = createPoll(db_sess, title, database.users.getUserId(username, password), unique, clauses) #if yes, creating poll
                database.users.updateUser(username, password, pollId) #updates user: adds poll to user.pollsCreated
                #notifying user that poll was created and giving instructions, how to share it
                flash('Poll created! To share poll, just copy this page link.', 'success')
                return redirect(url_for('pollpage', poll=pollId)) #redirecting user to polls route
            else: #if user is not in database
                raise UserException('User not found, log in account or create a new one') #creating error alert message
        except UserException as e: #if we receive user exception
            flash(f"{e}", "error") #creating alert itself
            return redirect(url_for(('createaccountpage')))#redirecting to create account route
    return render_template('create_poll.html') #returns create_poll.html template


if __name__ == "__main__":
    """here is the start of the program"""
    app.logger.addHandler(logging.StreamHandler(sys.stdout)) #heroku logs addition
    app.logger.setLevel(logging.ERROR) #heroku loggs addition
    app.run(debug=True) #running application