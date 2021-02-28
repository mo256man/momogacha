from flask import request, redirect, url_for, render_template, flash
from sqlalchemy.sql.expression import func
from models import Items #, Menu
import datetime
import random


# メイン
@app.route("/")
def main():
    items_left = db.session.query(Items).filter(Items.done==0).count()
    return render_template("test.html", left = items_left)






# ガチャの本番
def do_gatya():
    score = 0
    items = []
    for i in range(3):
        item =  db.session.query(Items).filter(Items.done==False).order_by(func.random()).first()
        price = my_function.kanji2num(item.kanji)
        item.done = True
        items.append([item.station, item.ken, item.item, item.kanji, item.id])
        score += price
        db.session.commit()

    items.sort(key=lambda x: x[4])
    kanji = my_function.num2kanji(score)
    return score, kanji, items

if __name__ == "__main__":
    app = Flask(__name__)
    db = SQLAlchemy(app)
    app.run(debug=True)
