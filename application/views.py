from flask import request, redirect, url_for, render_template, flash
from flask import make_response, send_from_directory
from sqlalchemy.sql.expression import func

from application import app, db
from application.models import Items
import application.my_function as my_function
import application.my_flexmsg as my_flexmsg
import application.my_line as my_line
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, FlexSendMessage

import datetime
import random

line_bot_api = LineBotApi("IWwLVAi1MJvj4uJ5XQdViLOnP977xP/vj+jzCJ1WBLMt4q4wDeq7fAIpMGE3WUY58Q204j4F6y45M6IW+OslP1+StpSdSEYIaounG9Fu3u/3arMZkxDREW3BggeKZFlB9IqQV5PKV9qsFbdRVip0fAdB04t89/1O/w1cDnyilFU=")  #チャネルアクセストークン
handler = WebhookHandler("631c484b9948356b740bd1ecc4ca8186")  #チャネルシークレット

# favicon
@app.route('/favicon.ico')
def favicon():
    return send_from_directory("static", "favicon.ico", )

# タイトル
@app.route("/", methods=["GET", "POST"])
def title():
    global uname
    uname = request.cookies.get("momoname")
    if (uname is None) or (uname==""):
        uname = random.choice(["ももたろ","きんたろ","うらしま"])
    return render_template("index.html", uname = uname)

# 名前変更
@app.route("/register_name", methods=["GET", "POST"])
def register_name():
    global uname
    if request.method == "POST":
        uname = request.form["uname"]
        response = make_response(render_template("index.html", uname=uname))
        response.set_cookie(key="momoname", value = uname)
    return response

# メイン
@app.route("/main", methods=["GET", "POST"])
def menu():
    last_day = 0

    if request.method == "GET":
        if request.args.get("reset"):
            items =  db.session.query(Items).filter(Items.done==1).all()
            for item in items:
                item.done = 0
            db.session.commit()
        elif request.args.get("return")=="True":
            with counter.get_lock():
                counter.value += 1
    else:
        pass

    uname = request.cookies.get("momoname")
#    cnt = counter.value
    today = datetime.datetime.today().day
    if today != last_day:
        items =  db.session.query(Items).filter(Items.done==1).all()
        for item in items:
            item.done = 0
        db.session.commit()
    last_day = today
    items_cnt = db.session.query(Items).count()
    items_left = db.session.query(Items).filter(Items.done==0).count()

    return render_template("main.html" ,
                             uname=uname, 
                             items_cnt=items_cnt, items_left=items_left,
                             today=today, last_day=last_day,
                             cnt = "cnt")


# ダイスを振る（デモ）
@app.route("/dice", methods=["GET", "POST"])
def dice():
    return render_template("dice.html")

# ガチャ
@app.route("/gatya", methods=["GET", "POST"])
def gatya():
    global cnt, all_results
    uname = request.cookies.get("momoname")
    dt = datetime.datetime.now().strftime("%Y/%m/%d")

    # 実行直前にもう一度物件数を確認する
    items_left = db.session.query(Items).filter(Items.done==False).count()
    if items_left < 3:
        return render_template("sorry.html")

    score = 0
    items = []
    for i in range(3):
        item =  db.session.query(Items).filter(Items.done==False).order_by(func.random()).first()
        price = my_function.kanji2num(item.kanji)
        item.done = 1
        items.append([item.station, item.ken, item.item, item.kanji, item.id])
        score += price
    db.session.commit()

    items.sort(key=lambda x: x[4])
    kanji = my_function.num2kanji(score)

    return render_template("result.html", uname=uname, result=items, score=kanji)



# 決算（富士山デモ）
@app.route("/kessan")
def kessan():
    return render_template("kessan.html")


# 決算（ランキング）
@app.route("/ranking", methods=["GET", "POST"])
def ranking():
    global df_items, all_results
    hiscore = sorted(all_results, key=lambda x:x["score"])[::-1][:3]
    return render_template("ranking.html", hiscore=hiscore)

# LINEのプロファイルを取得する
def get_profile(self, user_id, timeout=None):
    response = self._get(
        '/v2/bot/profile/{user_id}'.format(user_id=user_id),
        timeout=timeout)
    return Profile.new_from_json_dict(response.json)


@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)
    return 'OK'

# LINEでガチャをおこなう
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    id = event.source.user_id   #LINEのユーザーIDの取得
    txt = event.message.text
    if txt == "ガチャ！":
    #    today = datetime.datetime.now().strftime("%Y/%m/%d")
        profile = line_bot_api.get_profile(id)
        print (profile)
        # 日付更新を確認する
    #    if today != last_day:
    #       df_items["done"] = False
    #   last_day = today
        
        # 残物件数を確認する
        items_left = db.session.query(Items).filter(Items.done==False).count()
        if items_left < 3:
            payload = my_flexmsg.noItems()
        else:
            score = 0
            items = []
            for i in range(3):
                item =  db.session.query(Items).filter(Items.done==False).order_by(func.random()).first()
                price = my_function.kanji2num(item.kanji)
                item.done = 1
                items.append([item.station, item.ken, item.item, item.kanji, item.id])
                score += price
            db.session.commit()
            kanji = my_function.num2kanji(score)

            name = profile.display_name[0] + profile.display_name[-1] +"たろ社長"
            payload = my_flexmsg.get_payload(name, kanji, items)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=f"残り {items_left}"))
    elif txt == "決算！":
        payload = my_flexmsg.kessan()        
    
    else:
        payload = my_flexmsg.elsemsg()        

    container_obj = FlexSendMessage.new_from_json_dict(payload)
    line_bot_api.push_message(id, messages=container_obj)



# ガチャの本番
def do_gatya():
    score = 0
    items = []
    for i in range(3):
        item =  db.session.query(Items).filter(Items.done==False).order_by(func.random()).first()
        price = my_function.kanji2num(item.kanji)
        item.done = 1
        items.append([item.station, item.ken, item.item, item.kanji, item.id])
        score += price
        db.session.commit()

    items.sort(key=lambda x: x[4])
    kanji = my_function.num2kanji(score)
    return score, kanji, items
