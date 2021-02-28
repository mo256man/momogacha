from flask import Flask, request, abort, render_template
import json

from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import (MessageEvent, TextMessage, TextSendMessage, FlexSendMessage)

app = Flask(__name__)

line_bot_api = LineBotApi("IWwLVAi1MJvj4uJ5XQdViLOnP977xP/vj+jzCJ1WBLMt4q4wDeq7fAIpMGE3WUY58Q204j4F6y45M6IW+OslP1+StpSdSEYIaounG9Fu3u/3arMZkxDREW3BggeKZFlB9IqQV5PKV9qsFbdRVip0fAdB04t89/1O/w1cDnyilFU=")  #チャネルアクセストークン
handler = WebhookHandler("631c484b9948356b740bd1ecc4ca8186")  #チャネルシークレット

def get_profile(self, user_id, timeout=None):
    response = self._get(
        '/v2/bot/profile/{user_id}'.format(user_id=user_id),
        timeout=timeout)
    return Profile.new_from_json_dict(response.json)

@app.route("/", methods=['POST'])
def index():
    return render_template("index", name="aaa")

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

user = {}
# LINEでガチャをおこなう
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
    event.reply_token,
    TextSendMessage(text=event.message.text))
    """
    global df_items, cnt, all_results, last_day
    today = datetime.datetime.now().strftime("%Y/%m/%d")
    id = event.source.user_id   #LINEのユーザーIDの取得
    profile = line_bot_api.get_profile(id)

    # 日付更新を確認する
    if today != last_day:
        df_items["done"] = False
    last_day = today
    
    # 残物件数を確認する
    items_left = len(df_items[df_items["done"]==False])
    if items_left < 3:
        payload = my_flexmsg.noItems()
    else:
        df_items, result = my_function.do_gatya(df_items)
        item_list = result["table"]
        score = result["kanji"]

        name = profile.display_name
        random_cnt = int(len(name)*0.5)
        for i in range(random_cnt):
            pos = random.randint(1,len(name))
            if name[pos-1]!="＊":
                name = name.replace(name[:pos],name[:pos-1]+"＊")
            else:
                i -= 1
        payload = my_flexmsg.get_payload(name, score, item_list)

    container_obj = FlexSendMessage.new_from_json_dict(payload)
    line_bot_api.push_message(id, messages=container_obj)
    """