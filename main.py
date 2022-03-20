from flask import Flask, render_template, request, make_response, redirect, url_for, flash
import firebase_admin
from firebase_admin import credentials
import database.polls
import database.users
from utils.exceptions import *
import os.path
import json



app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'
app.secret_key = 'you wont hack this website cause youre stupid'

@app.route('/', methods=['POST', 'GET'])
def mainpage():
    return render_template('index.html')

@app.route('/account', methods=['POST', 'GET'])
def accountpage():
    username = request.cookies.get('username')
    password = request.cookies.get('password')
    if dbUser.checkUser(username, password):
        return render_template('account.html', username=username)
    else:
        return render_template('create_account.html')

@app.route('/create_account', methods=['POST', 'GET'])
def createaccountpage():
    username = request.cookies.get('username')
    password = request.cookies.get('password')
    if dbUser.checkUser(username, password):
        return redirect(url_for('accountpage'))
    if request.method == "POST":
        try:
            if "create_account" in request.form:
                password = request.form['password']
                username = request.form['username']
                if len(username) < 6 or len(password) < 6:
                    raise Exception('Length of username and pass must be longer than 5 symbols')
                if dbUser.create_user(password, username):
                    resp = make_response(redirect(url_for('accountpage')))
                    resp.set_cookie('username', username)
                    resp.set_cookie('password', password)
                    return resp
                else:
                    raise UserException('The user with this name already exists, log in account or choose another name')
            else:
                password = request.form['password_login']
                return render_template('create_account.html')
        except Exception as e:
            flash(f"{e}", "error")
            return render_template('create_account.html')

    return render_template('create_account.html')

@app.route('/poll', methods=['POST', 'GET'])
def pollpage():
    lockPoll = False
    password = request.cookies.get('password')
    username = request.cookies.get('username')
    if not dbUser.checkUser(username, password):
        return redirect(url_for('createaccountpage'))
    pollId = request.args.get('poll')
    poll = dbPolls.loadPoll(pollId)
    print(poll['isUnique'])
    if dbUser.getUserId(username) in poll['whoVoted']:
        lockPoll = True
    if request.method == "POST":
        answers = request.form.getlist('answer')
        if poll['isUnique'] and len(answers) > 1:
            flash('Do not try to cheat, little html hacker', 'error')
            return render_template('poll.html', poll=poll, isLocked=lockPoll)
        dbPolls.updatePoll(pollId, answers, username)
        flash(f"Thanks for voting!", "success")
        return redirect(url_for('mainpage'))
    return render_template('poll.html', poll=poll, isLocked=lockPoll)

@app.route('/create_poll', methods=['POST', 'GET'])
def createpollpage():
    if request.method == "POST":
        try:
            unique = True if request.form.get('isUnique') is None else False
            title = request.form.get('title')
            clauses=request.form.getlist('clause')
            username = request.cookies.get('username')
            password = request.cookies.get('password')
            if dbUser.checkUser(username, password):
                uid = dbUser.getUserId(username)
                pollId = dbPolls.create_poll(title, unique, clauses, uid)
                dbUser.updateUser(dbUser.getUserId(username), pollId)
                flash('Poll created! To share poll, just copy this page link.', 'success')
                return redirect(url_for('pollpage', poll=pollId))
            else:
                raise UserException('User not found, log in account or create a new one')
        except UserException as e:
            flash(f"{e}", "error")
            return render_template('create_account.html')
    return render_template('create_poll.html')


if __name__ == "__main__":
    """here is the start of the program"""
    if os.path.isfile('key.json'):
        cred = credentials.Certificate("key.json")
    else:
        creds_dict = json.loads(os.environ.get(("PRIVATE")))
        creds = credentials.Certificate(creds_dict)
    firebase_admin.initialize_app(cred)
    dbUser = database.users.DatabaseUser()
    dbPolls = database.polls.DatabasePoll()
    app.run(debug=True)