import math
import datetime

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

# 日付を文字列として取得する
def getStrDate():
  #  return datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    return datetime.datetime.now().strftime("%Y/%m/%d")

if __name__ == "__main__":
    pass
