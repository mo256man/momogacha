from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.sql.expression import func
from sqlalchemy import desc

import datetime
import application.my_function as my_function

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///momo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Items(db.Model):
    __tablename__ = "item"
    item = db.Column(db.String(32))
    kanji = db.Column(db.String(32))
    area = db.Column(db.String(32))
    ken = db.Column(db.String(32))
    station = db.Column(db.String(32))
    id = db.Column(db.Integer, primary_key=True)
    done = db.Column(db.Integer)

class Scores(db.Model):
    __tablename__ = "score"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    uname = db.Column(db.String)
    score = db.Column(db.Integer)
    item1 = db.Column(db.Integer)
    item2 = db.Column(db.Integer)
    item3 = db.Column(db.Integer)
    date = db.Column(db.String)

def resetItems():
    items = db.session.query(Items)
    # items.filter(Items.done == 1).done = 0
    # items.filter(Items.id < 0).done = 1
    items_done =  items.filter(Items.done==1).all()
    for item in items_done:
        item.done = 0
    items_example = items.filter(Items.id<0).all()
    for item in items_example:
        item.done = 1
    db.session.commit()

def count_all_items():
    cnt = db.session.query(Items).count()
    return cnt

def count_valid_items():
    cnt = db.session.query(Items).filter(Items.done==0).count()
    return cnt

def gacha(name, isLINE):
    global lastdate

    date = datetime.datetime.now().strftime("%Y/%m/%d")
    if date != lastdate:
        resetItems()
        lastdate = date

    if count_valid_items() < 3:
        print ("品切れです")

    # LINEの場合は匿名にする
    uname = name[0] + name[-1] + "たろ社長" if isLINE else name + "社長"

    # ガチャ
    score = 0
    result= []
    ids = []
    for i in range(3):
        item = db.session.query(Items).filter(Items.done==0).order_by(func.random()).first()
        price = my_function.kanji2num(item.kanji)
        item.done = 1
        ids.append(item.id)        
        result.append([item.station, item.ken, item.item, item.kanji, item.id])
        score += price
    db.session.commit()
    
    result.sort(key=lambda x: x[4])  # item.idで並び替え
    ids.sort()  # 一次元配列なので普通に並び替え
    kanji = my_function.num2kanji(score)

    dict = {}
    dict["name"] = name
    dict["uname"] = uname
    dict["score"] = score
    dict["item1"] = ids[0]
    dict["item2"] = ids[1]
    dict["item3"] = ids[2]
    dict["date"] = date
    db.session.execute(Scores.__table__.insert(), [dict])
    db.session.commit()
    return result

def getResult(id):
    item = db.session.query(Items).filter(Items.id==id).first()
    result = [item.station, item.ken, item.item, item.kanji, item.id]
    return result


def getScores():
    hiscores = db.session.query(Scores).order_by(Scores.score.desc()).limit(10).all()
    for hiscore in hiscores:
        uname = hiscore.uname
        score = hiscore.score
        print (uname, score)
        ids = []
        ids.append(hiscore.item1)
        ids.append(hiscore.item2)
        ids.append(hiscore.item3)
        for id in ids:
            result = getResult(id)
            print (id, result)

if __name__=="__main__":
    lastdate = "a"
    name = "ももたろ"
    isLINE = False
    result = gacha(name, isLINE)
    print (result)
    getScores()