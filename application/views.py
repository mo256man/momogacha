from flask import request, redirect, url_for, render_template, flash, send_file
from flask import make_response, send_from_directory
from sqlalchemy.sql.expression import func

import application
from application import app, db
import application.my_function as my_function
import application.my_flexmsg as my_flexmsg

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, FlexSendMessage

import datetime
import random

line_bot_api = LineBotApi("IWwLVAi1MJvj4uJ5XQdViLOnP977xP/vj+jzCJ1WBLMt4q4wDeq7fAIpMGE3WUY58Q204j4F6y45M6IW+OslP1+StpSdSEYIaounG9Fu3u/3arMZkxDREW3BggeKZFlB9IqQV5PKV9qsFbdRVip0fAdB04t89/1O/w1cDnyilFU = ")  #チャネルアクセストークン
handler = WebhookHandler("631c484b9948356b740bd1ecc4ca8186")  #チャネルシークレット
name = "" # グローバル変数

# favicon
@app.route('/favicon.ico')
def favicon():
    return send_from_directory("static", "favicon.ico", )

# タイトル
@app.route("/", methods = ["GET", "POST"])
def title():
    name = request.cookies.get("momoname")
    if (name is None) or (name == ""):
        name = random.choice(["ももたろ", "きんたろ", "うらしま", "やしゃ"])
    return render_template("index.html", name = name)

@app.route("/register_name", methods = ["GET", "POST"])
def register_name():
    name = request.cookies.get("momoname")
    if request.method == "POST":
        redirext = 1
        max_age = 60 * 60 * 24 * 7 # 7 days
        expires = int(datetime.datetime.now().timestamp()) + max_age
        name = request.form["name"]
    else:
        redirext = 0
    response = redirect(url_for("menu"))
    response.set_cookie(key = "momoname", value = name)
    return response

# メイン
@app.route("/main")
def menu():
    name = request.cookies.get("momoname")
    uname = name + "社長"
    my_function.checkDate()
    items_cnt = application.count_all_items()
    items_left = application.count_valid_items()

    return render_template("main.html" ,
                             uname = uname, 
                             items_cnt = items_cnt, items_left = items_left)

# アイテムを非選択状態に戻す（管理者専用）
@app.route("/reset_items")
def reset_items():
    application.resetItems()
    return redirect(url_for("menu"))

# ランキングを初期化する（管理者専用）
@app.route("/reset_score")
def reset_score():
    application.resetScore()
    return redirect(url_for("menu"))

# デイリーランキングのためのデモスコアの日付を今日にする（管理者専用）
@app.route("/refresh_score")
def refresh_score():
    application.refreshScore()
    return redirect(url_for("menu"))

# ダイスを振る（デモ）
@app.route("/dice")
def dice():
    return render_template("dice.html")

# webでガチャ
@app.route("/gacha")
def gacha():
    name = request.cookies.get("momoname")
    uname = name + "社長"
    kanji, result = application.do_gacha(name, uname, isLINE = False)
    # rank = application.get_rank()
    tweet_msg = my_function.get_tweet_msg(kanji, uname, result, isLine=False)
    return render_template("result.html", uname = uname, result = result, score = kanji ,tw_text = tweet_msg)


# 決算（富士山デモ）
@app.route("/kessan")
def kessan():
    return render_template("kessan.html")


# 決算（ランキング）
@app.route("/ranking", methods = ["GET", "POST"])
def ranking():
    if request.method == "GET":
        isDaily = 1 if request.args.get("daily") == "True" else 0
    name = request.cookies.get("momoname")
    uname = name + "社長"
    my_function.checkDate()
    results = application.get_scores(isDaily = isDaily)
    return render_template("ranking.html", uname = uname, results = results, isDaily = isDaily)


# おまけ
@app.route("/omake")
def omake():
    return render_template("omake.html")


# 管理人用
@app.route("/morishiman")
def morishiman():
    name = request.cookies.get("momoname")
    uname = name + "社長"
    my_function.checkDate()
    items_cnt = application.count_all_items()
    items_left = application.count_valid_items()
    return render_template("morishiman.html" ,
                             uname = uname, 
                             items_cnt = items_cnt, items_left = items_left)


# スコアデータのダウンロード
@app.route("/output_score")
def output_score():
    filename = application.downloadCSV()
    return send_file(f"static/{filename}", as_attachment = True)

# LINEのプロファイルを取得する
def get_profile(self, user_id, timeout = None):
    response = self._get("/v2/bot/profile/{user_id}".format(user_id = user_id), timeout = timeout)
    return Profile.new_from_json_dict(response.json)


# LINEコールバック
@app.route("/callback", methods = ['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text = True)
    app.logger.info("Request body: " + body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)
    return 'OK'


# LINEでコマンドを受ける
@handler.add(MessageEvent, message = TextMessage)
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
            kanji, result = application.do_gacha(name, uname, isLINE = True)
            payload = my_flexmsg.get_result(uname, kanji, result, isRanking=False)
        msg = f"残り {items_left}"

    elif txt == "決算！":
        my_function.checkDate()
        isDaily = random.choice([True, False])
        results = application.get_scores(isDaily = isDaily)
        payload = my_flexmsg.get_results(results, isRanking=True)
        msg = "決算【デイリー】" if isDaily else "決算【通期】"
        
    else:
        msg = ""
        payload = my_flexmsg.elsemsg()        

    if msg != "":
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text = msg))
  
    container_obj = FlexSendMessage.new_from_json_dict(payload)
    line_bot_api.push_message(id, messages = container_obj)
