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

def init():
    db.create_all()
