from flask import Flask, render_template, session, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from models import *
import sqlalchemy
import json
from sqlalchemy.ext.serializer import loads, dumps

app = Flask(__name__)
app.secret_key = 'any random string'
db = SQLAlchemy(app)
app.config["db"] = db

tests = {'test1': Test('2+3? Answers: a. 3, b. 4, c. 5', ["a. 3", "b. 4", "c. 5"], 'c'),
         'test2': Test('2*3? Answers: a. 3, b. 6, c. 7', ["a. 3", "b. 7", "c. 6"], 'b'),
         'test3': Test('2^3? Answers: a. 3, b. 8, c. 5', ["a. 3", "b. 7", "c. 6"], 'b'),
         'test4': Test('3+18/3? Answers: a. 13, b. 5, c. 9', ["a. 3", "b. 7", "c. 6"], 'c'),
         'test5': Test('4*5/20? Answers: a. 17, b. 5, c. 1', ["a. 3", "b. 7", "c. 6"], 'c')}
isAnswer = True

@app.route('/')
def index():
    if 'username' in session:
        return render_template('index.html', **{
            'username': session['username'],
            'loggedIn': True
        })
    return render_template('index.html', **{
        'loggedIn': False
    })


@app.route('/register', methods=('POST',))
def register():
    if 'username' not in request.form or 'email' not in request.form or 'password' not in request.form:
        return 'Missing parameters', 400
    user = dbsession.query(User).filter(User.username == request.form['username']).first()
    if not user:
        user = User(username=request.form['username'], password=request.form['password'], email=request.form['email'])
        dbsession.add(user)
        dbsession.commit()
        session['username'] = request.form['username']
        return '', 204
    return 'User already exists', 400


@app.route('/login', methods=('POST',))
def login():
    if 'username' not in request.form or 'password' not in request.form:
        return 'Missing parameters', 400
    user = dbsession.query(User).filter(User.username == request.form['username']).first()
    if user.password != request.form['password']:
        return 'Username or password is not valid', 400
    session['username'] = request.form['username']
    return '', 204


@app.route('/logout', methods=('POST',))
def logout():
    session.pop('username')
    return '', 204


@app.route('/account', methods=('POST',))
def add_account():
    if 'username' in session:
        user = dbsession.query(User).filter(User.username == session['username']).first()
        account = Account(name=request.form['name'], user_id=user.id)
        dbsession.add(account)
        dbsession.commit()
        return '', 204
    return 'Unauthorized', 401


@app.route('/home')
def home():
    if 'username' in session:
        accounts = dbsession.query(Account).join(User).filter(User.username == session['username']).all()
        shared_accounts = dbsession.query(Account).join(AccountMember).join(User).filter(
            User.username == session['username'] and AccountMember.user_id == User.id).all()
        allAccounts = dbsession.query(Account).all()

        return json.dumps({
            'accounts': [{
                'id': i.id,
                'name': i.name,
            } for i in accounts],
            'shared_accounts': [{
                'id': i.id,
                'name': i.name,
            } for i in shared_accounts],
            'all_accounts': [{
                'id': i.id,
                'name': i.name,
            } for i in allAccounts],
            'isAdmin': isAdmin(session['username'])
        })
    return 'Unauthorized', 401


def isAdmin(user):
    if (user == "admin"):
        return True
    return False


@app.route('/account/<id>')
def get_account(id):
    if 'username' not in session:
        return 'Unauthorized', 401
    account = dbsession.query(Account).join(User).filter(Account.id == id).first()
    if not account:
        return 'account missing', 400
    user = dbsession.query(User).filter(User.username == session['username']).first()
    account_members = dbsession.query(AccountMember).join(User).filter(AccountMember.account_id == account.id).all()
    member = [m for m in account_members if m.user_id == user.id]
    if account.user_id != user.id and not member and not isAdmin(session['username']):
        return 'user not in account', 400
    transactions = [{
        'id': i.id,
        'name': i.name,
        'amount': i.amount,
        'username': i.user.username
    } for i in dbsession.query(Transaction).join(User).filter(Transaction.account_id == id).all()]
    return json.dumps({
        'account': {
            'id': id,
            'name': account.name,
            'owner': account.user_id == user.id
        },
        'owner': account.user.username,
        'users': [{
            'username': m.user.username
        } for m in account_members],
        'transactions': transactions
    })


@app.route('/account', methods=('PUT',))
def update_account():
    if 'username' not in session:
        return 'Unauthorized', 401
    id = request.form['id']
    account = dbsession.query(Account).filter(Account.id == id).first()
    if not account:
        return 'account missing', 400
    user = dbsession.query(User).filter(User.username == session['username']).first()
    if account.user_id != user.id:
        return 'account missing', 400
    account.name = request.form['name']
    dbsession.commit()
    return '', 204


@app.route('/account', methods=('DELETE',))
def delete_account():
    if 'username' not in session:
        return 'Unauthorized', 401
    id = request.form['id']
    account = dbsession.query(Account).join(User).filter(
        Account.id == id and User.username == session['username']).first()
    if not account:
        return 'account missing', 400
    dbsession.query(AccountMember).filter(AccountMember.account_id == id).delete()
    dbsession.query(Transaction).filter(Transaction.account_id == id).delete()
    dbsession.delete(account)
    dbsession.commit()
    return '', 204


@app.route('/account_member', methods=('POST',))
def account_member_add():
    '''
    Add user to account
    id - account id
    username - user name
    '''
    if 'username' not in session:
        return 'Unauthorized', 401
    account = dbsession.query(Account).join(User).filter(
        User.username == session['username'] and Account.id == request.form['id']).first()
    if not account:
        return 'account missing', 400
    user = dbsession.query(User).filter(User.username == request.form['username']).first()
    if not user or user.username == session['username']:
        return 'user missing', 400
    account_member = AccountMember(user_id=user.id, account_id=account.id)
    dbsession.add(account_member)
    dbsession.commit()
    return jsonify({
        'id': user.id,
        'name': user.username
    })


@app.route('/account_member', methods=('DELETE',))
def account_member_remove():
    '''
    Remove user from account
    Params:
    id - account id
    userId - user id
    '''
    if 'username' not in session:
        return 'Unauthorized', 401
    account = dbsession.query(Account).join(User).filter(
        User.username == session['username'] and Account.id == request.form['id']).first()
    if not account:
        return 'account missing', 400
    dbsession.query(AccountMember).filter(
        AccountMember.user_id == request.form['userId'] and AccountMember.account_id == request.form['id']).delete()
    dbsession.commit()
    return '', 204

@app.route('/add_transaction', methods=('POST',))
def add_transaction():
    '''newId = id%tests.__sizeof__()'''
    if 'username' not in session:
        return 'Unauthorized', 401
    user = dbsession.query(User).filter(User.username == session['username']).first()
    transaction = Transaction(name=request.form['name'], amount=request.form['amount'], user_id=user.id,
                              account_id=request.form['account_id'])
    dbsession.add(transaction)
    admin = dbsession.query(User).filter(User.username == 'username').first()
    userAnswer = request.form['name']
    if len(userAnswer) > 1 :
        if tests.__contains__(userAnswer):
            test = tests[userAnswer]
            message = test.Question
            transaction = Transaction(name=message, amount=0, user_id=2,
                                      account_id=request.form['account_id'])
            dbsession.add(transaction)
    else:
        testKey = 'test1'
        test = tests[testKey]
        userAnswer = request.form['name']
        if userAnswer != 'a':
            transaction = Transaction(name='Yes', amount=0, user_id=2,
                                      account_id=request.form['account_id'])
            dbsession.add(transaction)
        else:
            transaction = Transaction(name='No', amount=0, user_id=2,
                                      account_id=request.form['account_id'])
            dbsession.add(transaction)


    dbsession.commit()
    return '', 204


if __name__ == "__main__":
    app.run()
