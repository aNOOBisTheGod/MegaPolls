from flask import Flask, render_template, request, make_response, redirect, url_for, flash
import firebase_admin
from firebase_admin import credentials
from database.polls import createPoll, getPollJson, voteInPoll
from utils.exceptions import *
import os.path
import json
from database import db_session
import database.users
import logging
import sys



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
    if request.method == "POST":
        resp = make_response(redirect(url_for('createaccountpage')))
        resp.set_cookie('username', '0')
        resp.set_cookie('password', '0')
        return resp
    if database.users.checkUser(username, password):
        return render_template('account.html', username=username)
    else:
        print('Wrong')
        return redirect(url_for(('createaccountpage')))

@app.route('/create_account', methods=['POST', 'GET'])
def createaccountpage():
    username = request.cookies.get('username')
    password = request.cookies.get('password')
    if database.users.checkUser(username, password):
        return redirect(url_for('accountpage'))
    if request.method == "POST":
        try:
            if "create_account" in request.form:
                print('creating add')
                password = request.form['password']
                username = request.form['username']
                if len(username) < 6 or len(password) < 6:
                    raise Exception('Length of username and pass must be longer than 5 symbols')
                user = database.users.User()
                user.username = username
                user.password = password
                user.pollsCreated = ''
                db_sess.add(user)
                db_sess.commit()
                resp = make_response(redirect(url_for('accountpage')))
                resp.set_cookie('username', username)
                resp.set_cookie('password', password)
                return resp
            else:
                username = request.form['username_login']
                password = request.form['password_login']
                print(username, password, database.users.checkUser(username, password))
                if database.users.checkUser(username, password):
                    resp = make_response(redirect(url_for('accountpage')))
                    resp.set_cookie('username', username)
                    resp.set_cookie('password', password)
                    return resp
                else:
                    raise UserException('User not found! Make sure username and password are correct')
        except Exception as e:
            flash(f"{e}", "error")
            return render_template('create_account.html')

    return render_template('create_account.html')

@app.route('/poll', methods=['POST', 'GET'])
def pollpage():
    lockPoll = False
    password = request.cookies.get('password')
    username = request.cookies.get('username')
    if not database.users.checkUser(username, password):
        return redirect(url_for('createaccountpage'))
    pollId = request.args.get('poll')
    poll = getPollJson(db_sess, pollId)
    if database.users.getUserId(username, password) in poll['whoVoted']:
        lockPoll = True
    if request.method == "POST":
        answers = request.form.getlist('answer')
        if poll['isUnique'] and len(answers) > 1:
            flash('Do not try to cheat, little html hacker', 'error')
            return render_template('poll.html', poll=poll, isLocked=lockPoll)
        voteInPoll(db_sess, pollId, database.users.getUserId(username, password), answers)
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
            if database.users.checkUser(username, password):
                pollId = createPoll(db_sess, title, database.users.getUserId(username, password), unique, clauses)
                database.users.updateUser(username, password, pollId)
                flash('Poll created! To share poll, just copy this page link.', 'success')
                return redirect(url_for('pollpage', poll=pollId))
            else:
                raise UserException('User not found, log in account or create a new one')
        except UserException as e:
            flash(f"{e}", "error")
            return redirect(url_for(('createaccountpage')))
    return render_template('create_poll.html')


if __name__ == "__main__":
    """here is the start of the program"""
    db_session.global_init("db/data.db")
    db_sess = db_session.create_session()
    app.logger.addHandler(logging.StreamHandler(sys.stdout))
    app.logger.setLevel(logging.ERROR)
    app.run(debug=True)