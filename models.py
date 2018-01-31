from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, Float, create_engine
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()

class Test():
    Question = ""
    Answers = []
    RightAnswer = ""
    def __init__(self, question, answers, rightAnswer):
        self.Question = question
        self.Answers = answers,
        self.RightAnswer = rightAnswer

    def checkAnswer(self, answer):
        if self.RightAnswer == answer:
            return True


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    email = Column(String)
    password = Column(String)


class Chat(Base):
    __tablename__ = 'chats'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User")


class Message(Base):
    __tablename__ = 'messages'
    id = Column(Integer, primary_key=True)
    message = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))
    chat_id = Column(Float, ForeignKey('chats.id'))
    user = relationship("User")


class ChatMember(Base):
    __tablename__ = 'chat_members'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    chat_id = Column(Integer, ForeignKey('chats.id'))
    user = relationship("User")

engine = create_engine('postgres://postgres:Romeo702@localhost:5432/postgres1', echo=True)
engine.connect()
Session = sessionmaker(bind=engine)
dbsession = Session()
