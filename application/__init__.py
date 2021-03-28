from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.sql.expression import func
from sqlalchemy import desc

import os
import datetime
import pandas as pd
import pandas.io.sql as psql
import application.my_function as my_function

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///momo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Items(db.Model):
    __tablename__ = "item"
    item = db.Column(db.String(32))
    kanji = db.Column(db.String(32))
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
    time = db.Column(db.String)

# アイテムを非選択状態に戻す
def resetItems():
    items = db.session.query(Items)
    items_done =  items.filter(Items.done==1).all()
    # sqliteはwhere条件で一気に更新はできない？
    for item in items_done:
        item.done = 0
    items_example = items.filter(Items.id<0).all()
    for item in items_example:
        item.done = 1
    db.session.commit()

# ランキングを初期化する
def resetScore():
    db.session.query(Scores).filter(Scores.id>0).delete()
    date = my_function.getStrDate()
    scores = db.session.query(Scores).all()
    for score in scores:
        score.date = date
    db.session.commit()

def refreshScore():
    scores = db.session.query(Scores).filter(Scores.id<=0)
    date = my_function.getStrDate()
    for score in scores:
        score.date = date
    db.session.commit()

def count_all_items():
    cnt = db.session.query(Items).filter(Items.id>0).count()
    return cnt

def count_valid_items():
    cnt = db.session.query(Items).filter(Items.done==0).count()
    return cnt

def get_last_date():
    lastdate = db.session.query(Scores).order_by(Scores.id.desc()).first().date
    return lastdate

def do_gacha(name, uname, isLINE):
    last_date = get_last_date()
    today = my_function.getStrDate()
    time = my_function.getStrTime()
    if today != last_date:
        resetItems()
        last_date = today

    if count_valid_items() < 3:
        print ("品切れです")

    # ガチャ
    score = 0
    result= []
    ids = []
    for i in range(3):
        item =  db.session.query(Items).filter(Items.done==0).order_by(func.random()).first()
        price = my_function.kanji2num(item.kanji)
        item.done = 1
        ids.append(item.id)
        result.append([item.item, item.station, item.ken, item.kanji, item.id])
        score += price
    db.session.commit()

    result.sort(key=lambda x: x[4])  # 4番目の要素すなわちitem.idで並び替え
    ids.sort()                       # 一次元配列なので普通に並び替え
    kanji = my_function.num2kanji(score)

    dict = {}
    dict["name"] = name
    dict["uname"] = uname
    dict["score"] = score
    dict["item1"] = ids[0]
    dict["item2"] = ids[1]
    dict["item3"] = ids[2]
    dict["date"] = today
    dict["time"] = time
    db.session.execute(Scores.__table__.insert(), [dict])
    db.session.commit()
    return kanji, result

def id2item(id):
    item = db.session.query(Items).filter(Items.id==id).first()
    result = [item.item, item.station, item.ken, item.kanji, item.id]
    return result

def get_scores(isDaily):
    results = []
    scores = db.session.query(Scores)
    if isDaily:
        today = my_function.getStrDate()
        topdata = scores.filter(Scores.date==today).order_by(Scores.score.desc()).limit(5).all()
    else:
        topdata = scores.order_by(Scores.score.desc()).limit(5).all()

    for data in topdata:
        result = {}
        result["name"] = data.name
        result["uname"] = data.uname
        result["date"] = data.date
        result["time"] = data.time
        result["kanji"] = my_function.num2kanji(data.score)
        items = []        
        for id in [data.item1, data.item2, data.item3]:
            item = id2item(id)
            items.append(item)
        result["table"] = items
        results.append(result)
    return results

def get_rank():
    # 参考　https://www.javaer101.com/fr/article/1022365.html
    scores = db.session.query(Scores)
    id = scores.order_by(Scores.id.desc()).first().id

    subquery = db.session.query(Scores,
        func.rank().over(
            order_by = Scores.score.desc()
#            partition_by = Scores.id
            ).label('rnk')
    ).subquery()
    query = db.session.query(subquery).all()  # listになる
    rank = [x.rnk for x in query if x.id == id][0]
    return rank

def downloadCSV():
    time = my_function.getStrTime()
    print (time)
    filename = f"momo_score_{time}.csv"
    os.chdir("application/static/")
    df = pd.read_sql(db.session.query(Scores).statement,db.session.bind)
    df.to_csv(filename, index=False, sep=",", encoding="utf_8_sig", mode="w")
    return filename
    
import application.views