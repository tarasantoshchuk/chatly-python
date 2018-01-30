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


class Account(Base):
    __tablename__ = 'financial_accounts'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User")


class Transaction(Base):
    __tablename__ = 'transactions'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    amount = Column(Float)
    user_id = Column(Integer, ForeignKey('users.id'))
    account_id = Column(Float, ForeignKey('financial_accounts.id'))
    user = relationship("User")


class AccountMember(Base):
    __tablename__ = 'account_members'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    account_id = Column(Integer, ForeignKey('financial_accounts.id'))
    user = relationship("User")

engine = create_engine('postgres://postgres:qwerty@localhost:5433/postgres', echo=True)
engine.connect()
Session = sessionmaker(bind=engine)
dbsession = Session()
