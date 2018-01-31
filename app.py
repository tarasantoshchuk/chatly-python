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


@app.route('/chat', methods=('POST',))
def add_chat():
    if 'username' in session:
        user = dbsession.query(User).filter(User.username == session['username']).first()
        chat = Chat(name=request.form['name'], user_id=user.id)
        dbsession.add(chat)
        dbsession.commit()
        return '', 204
    return 'Unauthorized', 401


@app.route('/home')
def home():
    if 'username' in session:
        chats = dbsession.query(Chat).join(User).filter(User.username == session['username']).all()
        shared_chats = dbsession.query(Chat).join(ChatMember).join(User).filter(
            User.username == session['username'] and ChatMember.user_id == User.id).all()
        allChats = dbsession.query(Chat).all()

        return json.dumps({
            'chats': [{
                'id': i.id,
                'name': i.name,
            } for i in chats],
            'shared_chats': [{
                'id': i.id,
                'name': i.name,
            } for i in shared_chats],
            'all_chats': [{
                'id': i.id,
                'name': i.name,
            } for i in allChats],
            'isAdmin': isAdmin(session['username'])
        })
    return 'Unauthorized', 401


def isAdmin(user):
    if (user == "admin"):
        return True
    return False


@app.route('/chat/<id>')
def get_ac(id):
    if 'username' not in session:
        return 'Unauthorized', 401
    chat = dbsession.query(Chat).join(User).filter(Chat.id == id).first()
    if not chat:
        return 'chat missing', 400
    user = dbsession.query(User).filter(User.username == session['username']).first()
    chat_members = dbsession.query(ChatMember).join(User).filter(ChatMember.chat_id == chat.id).all()
    member = [m for m in chat_members if m.user_id == user.id]
    if chat.user_id != user.id and not member and not isAdmin(session['username']):
        return 'user not in chat', 400
    messages = [{
        'id': i.id,
        'message': i.message,
        'username': i.user.username
    } for i in dbsession.query(Message).join(User).filter(Message.chat_id == id).all()]
    return json.dumps({
        'chat': {
            'id': id,
            'name': chat.name,
            'owner': chat.user_id == user.id
        },
        'owner': chat.user.username,
        'users': [{
            'username': m.user.username
        } for m in chat_members],
        'messages': messages
    })


@app.route('/chat', methods=('PUT',))
def update_chat():
    if 'username' not in session:
        return 'Unauthorized', 401
    id = request.form['id']
    chat = dbsession.query(Chat).filter(Chat.id == id).first()
    if not chat:
        return 'chat missing', 400
    user = dbsession.query(User).filter(User.username == session['username']).first()
    if chat.user_id != user.id:
        return 'chat missing', 400
    chat.name = request.form['name']
    dbsession.commit()
    return '', 204


@app.route('/chat', methods=('DELETE',))
def delete_chat():
    if 'username' not in session:
        return 'Unauthorized', 401
    id = request.form['id']
    chat = dbsession.query(Chat).join(User).filter(
        Chat.id == id and User.username == session['username']).first()
    if not chat:
        return 'chat missing', 400
    dbsession.query(ChatMember).filter(ChatMember.chat_id == id).delete()
    dbsession.query(Message).filter(Message.chat_id == id).delete()
    dbsession.delete(chat)
    dbsession.commit()
    return '', 204


@app.route('/chat_member', methods=('POST',))
def chat_member_add():
    '''
    Add user to chat
    id - chat id
    username - user name
    '''
    if 'username' not in session:
        return 'Unauthorized', 401
    print '_________________________________'
    print request.form['id']
    chat = dbsession.query(Chat).filter(Chat.id == request.form['id']).first()
    if not chat:
        return 'chat missing', 400
    user = dbsession.query(User).filter(User.username == request.form['username']).first()
    if not user or user.username == session['username']:
        return 'user missing', 400
    print '_________________________________'
    print chat.id
    print user.id
    chat_member = ChatMember(user_id=user.id, chat_id=chat.id)
    dbsession.add(chat_member)
    dbsession.commit()
    return jsonify({
        'id': user.id,
        'name': user.username
    })


@app.route('/chat_member', methods=('DELETE',))
def chat_member_remove():
    '''
    Remove user from chat
    Params:
    id - chat id
    userId - user id
    '''
    if 'username' not in session:
        return 'Unauthorized', 401
    chat = dbsession.query(Chat).join(User).filter(
        User.username == session['username'] and Chat.id == request.form['id']).first()
    if not chat:
        return 'chat missing', 400
    dbsession.query(ChatMember).filter(
        ChatMember.user_id == request.form['userId'] and ChatMember.chat_id == request.form['id']).delete()
    dbsession.commit()
    return '', 204

@app.route('/add_message', methods=('POST',))
def add_message():
    '''newId = id%tests.__sizeof__()'''
    if 'username' not in session:
        return 'Unauthorized', 401
    user = dbsession.query(User).filter(User.username == session['username']).first()
    message = Message(message=request.form['message'], user_id=user.id,
                              chat_id=request.form['chat_id'])
    dbsession.add(message)
    bot = dbsession.query(User).filter(User.username == 'bot').first()
    hasChatBot = dbsession.query(ChatMember).filter(ChatMember.chat_id == request.form['chat_id']).filter(ChatMember.user_id == bot.id).all()

    userAnswer = request.form['message']
    if len(hasChatBot) > 0:
        if userAnswer == 'help':
            botMessage = Message(message='Please choose test in format: "test + number of test".\n'
                                         'Amount of test = {:d}'.format(len(tests)), user_id=bot.id,
                                 chat_id=request.form['chat_id'])
            dbsession.add(botMessage)
        if len(userAnswer) > 1:
            if tests.__contains__(userAnswer):
                test = tests[userAnswer]
                message = test.Question
                botMessage = Message(message=message, user_id=bot.id,
                                     chat_id=request.form['chat_id'])
                dbsession.add(botMessage)
        if ['a', 'b', 'c'].__contains__(userAnswer):
            lastMessage = dbsession.query(Message).filter(Message.user_id == bot.id).order_by('-id').first()
            rightAnswer = 'x'
            for test in tests:
                if tests[test].Question == lastMessage.message:
                    rightAnswer = tests[test].RightAnswer
            if userAnswer == rightAnswer and rightAnswer != 'x':
                botMessage = Message(message='Yes, you are right', user_id=bot.id,
                                     chat_id=request.form['chat_id'])
                dbsession.add(botMessage)
            elif rightAnswer == 'x':
                print ''
            else:
                botMessage = Message(message='No, the right answer is: '+ rightAnswer, user_id=bot.id,
                                     chat_id=request.form['chat_id'])
                dbsession.add(botMessage)

    dbsession.commit()
    return '', 204


if __name__ == "__main__":
    app.run()
