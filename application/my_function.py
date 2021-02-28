import math
import datetime
from application import app, db

"""
# インデックスから物件リストを作る
def index2list(df, items):
    item_list = []
    for i in items:
        station = df.at[i,"station"]
        ken = df.at[i,"ken"]
        item = df.at[i,"item"]
        kanji = df.at[i,"kanji"]
        item_list.append([station, ken, item, kanji])
    return item_list
"""
"""
# ガチャの本番（df）
def df_gatya(df):
    score = 0
    item3 = []
    for i in range(3):
        index = df[df["done"] == False].sample().index[0]
        item3.append(index)
        df.at[index, "done"] = True
        price = kanji2num(df.at[index, "kanji"])
        score += price
    kanji = num2kanji(score)
    item3.sort()
    item_list = index2list(df, item3)
    result = {"score":score, "kanji":kanji, "items":item3, "table":item_list}
    return df, result
"""

# 文字列パーセントを小数にする
def p2f(x):
    return float(x.strip("%"))/100


# 数値を漢字にする
def num2kanji(number):
    units = ["", "万", "億", "兆", "京", "垓", "𥝱"]
    str_num = str(number)
    keta = math.ceil((len(str_num)/4))*4
    str_num = str(str_num).zfill(keta)
    keta = keta//4
    kanji = ""
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

if __name__ == "__main__":
    pass
