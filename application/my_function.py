import math
import datetime
import pytz
import urllib.parse
import application

# 数値を漢字にする　面倒なので0は特別扱い
def num2kanji(number):
    if number == 0:
        kanji = "0"
    else:
        kanji = ""
        units = ["", "万", "億", "兆", "京", "垓", "𥝱"]
        str_num = str(number)
        keta = math.ceil((len(str_num)/4))*4
        str_num = str(str_num).zfill(keta)
        keta = keta//4
        for i in range(0, keta):
            num = int(str_num[i*4:(i+1)*4])
            if num != 0:
                kanji += f"{num}{units[keta-i-1]}"
    return kanji


# 漢字を数値にする
def kanji2num(kanji):
    units = ["一","万", "億", "兆", "京", "垓", "𥝱"]
    number = 0

    if kanji[-1]=="円":
          kanji = kanji[:-1]

    tmp = kanji + "一"
    for x in units:
        tmp = tmp.replace(x, x+",")
    if tmp[-1] == ",":
        tmp = tmp[:-1]
    list_kanji = tmp.split(",")

    for k in list_kanji[:-1]:
        for i,x in enumerate(units):
            if x in k:
                number += int(k[:-1]) * 10**(4*i)

    if list_kanji[-1] != "一":
        number += int(list_kanji[-1][:-1])

    return number


# 日付変更チェック
def checkDate():
    last_date = application.get_last_date()
    today = getStrDate()
    if today != last_date:
        application.resetItems()
        application.refreshScore()
    return


# 日付を文字列として取得する
def getStrDate():
    jst = pytz.timezone("Asia/Tokyo")
    return datetime.datetime.now(jst).strftime("%Y/%m/%d")


# 時刻を文字列として取得する
def getStrTime():
    jst = pytz.timezone("Asia/Tokyo")
    return datetime.datetime.now(jst).strftime("%H:%M:%S")


# 半角数字を全角にする力業
# 参考　https://qiita.com/YuukiMiyoshi/items/6ce77bf402a29a99f1bf
def han2zen(txt):
    return txt.translate(str.maketrans({chr(0x0021 + i): chr(0xFF01 + i) for i in range(94)}))


# Twitter用の文を作成する
def get_tweet_msg(kanji, uname, result, isLine):
    tmp = [han2zen(kanji)+"円"]
    for row in result:
        tmp.append(han2zen(row[3]))
    max_len = max(len(x) for x in tmp)
    tweet_msg = f"#桃鉄ガチャ　　{uname}\n"
    if isLine:
        tweet_msg += f"【スコア　　　{kanji} 円】\n\n"
    else:
        tweet_msg += "【スコア　　" + "　" * (max_len-len(tmp[0])) + tmp[0] + "】\n\n"
    
    for i in [1,2,3]:
        if isLine:
            tweet_msg += f"{result[i-1][0]}（{result[i-1][3]}）\n"
        else:
            tweet_msg += f"{result[i-1][0]}（{result[i-1][1]}）\n"
            tweet_msg +=  "　" * (max_len-len(tmp[i]) + 6) + tmp[i] + "\n"

    tweet_msg = urllib.parse.quote(tweet_msg)
    return tweet_msg

if __name__ == "__main__":
    pass
