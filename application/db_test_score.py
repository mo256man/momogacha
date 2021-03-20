from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.sql.expression import func

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///score.db"
db = SQLAlchemy(app)

class Score(Base):
      __tablename__ = "score"
  number = Column(Integer, primary_key=True)
  uname = Column(String)
  kanji = Column(String)
  id1 = Column(Integer)
  id2 = Column(Integer)
  id3 = Column(Integer)
  date = Column(String)

  def __init__(self,
               uname = None,
               kanji = None,
               id1 = None,
               id2 = None,
               id3 = None,
               date = None):
    self.uname = uname
    self.kanji = kanji
    self.id1 = id1
    self.id2 = id2
    self.id3 = id3
    self.date = date

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

print (db.session.query(Score).count())

"""
# ランダムな一つをdone=1にする（ガチャ）
for i in range(100):
    item =  db.session.query(Items).filter(Items.done==0).order_by(func.random()).first()
    print("random item no=", item.id)
    print(item.station, item.ken, item.item, item.kanji)
    item.done = 1

db.session.commit()

print (db.session.query(Items).filter(Items.done==0).count())

"""

