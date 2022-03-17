from flask import Flask, render_template, request, make_response, redirect, url_for, flash
import firebase_admin
from firebase_admin import credentials
import database.polls
import database.users
from utils.errors import *
from firebase_admin import auth

app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'
app.secret_key = 'super secret key'

@app.route('/', methods=['POST', 'GET'])
def mainpage():
    return render_template('index.html')

@app.route('/account', methods=['POST', 'GET'])
def accountpage():
    username = request.cookies.get('username')
    password = request.cookies.get('password')
    if database.users.checkUser(username, password):
        return render_template('account.html', username=username)
    else:
        return render_template('create_account.html')

@app.route('/create_account', methods=['POST', 'GET'])
def createaccountpage():
    username = request.cookies.get('username')
    password = request.cookies.get('password')
    if database.users.checkUser(username, password):
        return redirect(url_for('accountpage'))
    if request.method == "POST":
        try:
            if "create_account" in request.form:
                print('exception here!')
                password = request.form['password']
                username = request.form['username']
                if len(username) < 6 or len(password) < 6:
                    raise Exception('Length of username and pass must be longer than 5 symbols')
                if database.users.create_user(password, username):
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
def data():
    lockPoll = False
    password = request.cookies.get('password')
    if database.users.checkUser(username, password):
        username = request.cookies.get('username')
    else: 
        return redirect(url_for('createaccountpage'))
    pollId = request.args.get('poll')
    poll = database.polls.loadPoll(pollId)
    if database.users.getUserId(username) in poll['whoVoted']:
        lockPoll = True
    if request.method == "POST":
        answers = request.form.getlist('answer')
        database.polls.updatePoll(pollId, answers, username)
        return redirect(url_for('mainpage'))
    return render_template('poll.html', poll=poll, isLocked=lockPoll)

@app.route('/create_poll', methods=['POST', 'GET'])
def createpollpage():
    if request.method == "POST":
        try:
            an = False if request.form.get('anonymous') is None else True
            title = request.form.get('title')
            clauses=request.form.getlist('clause')
            username = request.cookies.get('username')
            password = request.cookies.get('password')
            if database.users.checkUser(username, password):
                uid = database.users.getUserId(username)
                database.polls.create_poll(title, an, clauses, uid)
            else:
                raise UserException()
        except UserException as e:
            flash(f"{e}", "error")
            return render_template('create_account.html')
    return render_template('create_poll.html')


if __name__ == "__main__":
    cred = credentials.Certificate("key.json")
    firebase_admin.initialize_app(cred)
    
    app.run(debug=True)
    