from flask import request, redirect, url_for, render_template, flash
from flask import make_response, send_from_directory
from sqlalchemy.sql.expression import func

import application
from application import app, db
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
    uname = request.cookies.get("momoname")
    last_date = application.get_last_date()
    
    if request.method == 'GET':
        if request.args.get("resetItems", ""):
            application.resetItems()  
        if request.args.get("resetScore", ""):
            application.resetScore()  
    
    today = my_function.getStrDate()
    if today != last_date:
        application.resetItems()
    last_date = today

    items_cnt = application.count_all_items()
    items_left = application.count_valid_items()

    return render_template("main.html" ,
                             uname=uname, 
                             items_cnt=items_cnt, items_left=items_left,
                             today=today, last_day=last_date)


# ダイスを振る（デモ）
@app.route("/dice", methods=["GET", "POST"])
def dice():
    return render_template("dice.html")

# webでガチャ
@app.route("/gatya", methods=["GET", "POST"])
def gatya():
    name = request.cookies.get("momoname")
    uname = name + "社長"
    kanji, result = application.do_gacha(name, uname, isLINE=False)
    return render_template("result.html", uname=uname, result=result, score=kanji)

# 決算（富士山デモ）
@app.route("/kessan")
def kessan():
    return render_template("kessan.html")


# 決算（ランキング）
@app.route("/ranking", methods=["GET", "POST"])
def ranking():
    results = application.get_scores()
    return render_template("ranking.html", results=results)

# LINEのプロファイルを取得する
def get_profile(self, user_id, timeout=None):
    response = self._get(
        '/v2/bot/profile/{user_id}'.format(user_id=user_id),
        timeout=timeout)
    return Profile.new_from_json_dict(response.json)

# LINEコールバック
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

# LINEでコマンドを受ける
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    id = event.source.user_id   #LINEのユーザーIDの取得
    profile = line_bot_api.get_profile(id)
    name = profile.display_name
    uname = name[0] + name[-1] +"たろ社長"
    txt = event.message.text
    if txt == "ガチャ！":
        items_left = application.count_valid_items()        
        if items_left < 3:
            payload = my_flexmsg.noItems()
        else:
            kanji, result = application.do_gacha(name, uname, isLINE=True)
            payload = my_flexmsg.get_result(uname, kanji, result)

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=f"残り {items_left}"))
    elif txt == "決算！":
        results = application.get_scores()
        payload = my_flexmsg.get_results(results)
    else:
        payload = my_flexmsg.elsemsg()        

    container_obj = FlexSendMessage.new_from_json_dict(payload)
    line_bot_api.push_message(id, messages=container_obj)

