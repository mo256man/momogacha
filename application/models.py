from application import db
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

class Items(db.Model):
    __tablename__ = "item"
    item = db.Column(db.String(32))
    kanji = db.Column(db.String(32))
    area = db.Column(db.String(32))
    ken = db.Column(db.String(32))
    station = db.Column(db.String(32))
    id = db.Column(db.Integer, primary_key=True)
    done = db.Column(db.Integer)

class Score(db.Model):
    __tablename__ = "score"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    uname = db.Column(db.String)
    score = db.Column(db.Integer)
    item1 = db.Column(db.Integer)
    item2 = db.Column(db.Integer)
    item3 = db.Column(db.Integer)
    date = db.Column(db.String)

def init():
    db.create_all()

