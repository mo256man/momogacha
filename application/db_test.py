from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.sql.expression import func

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///momo.db"
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

"""
# この部分、成功している。消すな
from sqlalchemy import create_engine
engine = create_engine("sqlite:///momo.db")

from sqlalchemy import inspect
inspector = inspect(engine)

for table_name in inspector.get_table_names():
    print ()
    print (table_name)
    for column in inspector.get_columns(table_name):
       print("Column: %s" % column['name'])
"""

#engine = create_engine("sqlite:///momo.db")
#SessionClass=sessionmaker(engine)
#session=SessionClass()

#for item in session.query(Items).all():
#  print(item.item, item.kanji)

print (db.session.query(Items).filter(Items.done==0).count())

# ランダムな一つをdone=1にする（ガチャ）
for i in range(100):
    item =  db.session.query(Items).filter(Items.done==0).order_by(func.random()).first()
    print("random item no=", item.id)
    print(item.station, item.ken, item.item, item.kanji)
    item.done = 1

db.session.commit()

print (db.session.query(Items).filter(Items.done==0).count())
