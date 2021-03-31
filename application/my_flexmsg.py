import application.my_function as my_function

def get_contents_item(item):
  contents_item = {
    "type": "box",
    "layout": "horizontal",
    "contents": [{
      "type": "text",
      "text": item[0],
      "color": "#111111",
      "flex": 0,
      "size": "lg"}]}
  return contents_item

def get_contents_score(item):
  contents_score = {
    "type": "box",
    "layout": "horizontal",
    "contents": [{
      "type": "text",
      "text": item[1] + "（" + item[2] + "）",
      "size": "md",
      "color": "#111111",
      "flex": 0}, {
      "type": "text",
      "text": item[3],
      "size": "md",
      "color": "#111111",
      "align": "end"}]}
  return contents_score      

def get_dict_link(name, kanji, result):
  tweet_msg = my_function.get_tweet_msg(kanji, name, result, isLine=True)
  tweet_url = "https://twitter.com/intent/tweet?text=" + tweet_msg

  dict_link = {
    "type": "box",
    "layout": "vertical",
    "contents": [{
      "type": "filler"
    },{
      "type": "box",
      "layout": "baseline",
      "contents": [{
        "type": "filler"
      },{
        "type": "text",
        "text": "Tweet!",
        "color": "#ffffff",
        "flex": 0,
        "offsetTop": "-2px",
        "align": "center",
        "weight": "bold"
      },{
        "type": "filler"
      }],
      "spacing": "sm",
      "action": {
        "type": "uri",
        "label": "action",
        "uri": tweet_url
      }
    },{
      "type": "filler"
      }],
      "borderWidth": "3px",
      "cornerRadius": "5px",
      "spacing": "sm",
      "margin": "xxl",
      "height": "40px",
      "borderColor": "#1da1f2",
      "backgroundColor": "#1da1f2"
    }

  return dict_link

def get_dict_body(name, kanji, item_list, isRanking, i):
  if isRanking:
    name = f"{i+1}位　{name}"

  dict_name = {
    "type": "text",
    "text": name,
    "weight": "bold",
    "size": "xl"}

  dict_score = {
    "type": "text",
    "text": kanji + "円",
    "wrap": True,
    "align": "end",
    "size": "lg",
    "color": "#000000",
    "weight": "bold"}

  dict_separator = {
    "type": "separator",
    "margin": "md",
    "color": "#808080"}

  dict_contents = []
  for item in item_list:
    content_item = get_contents_item(item)      
    content_score = get_contents_score(item)
    dict_contents.append(
      { "type": "box",
        "layout": "vertical",
        "margin": "xxl",
        "spacing": "sm",
        "contents": [content_item, content_score]
      })

  contents = [dict_name,
              dict_score,
              dict_separator,
              dict_contents[0],
              dict_contents[1],
              dict_contents[2]]

  if not isRanking:
    dict_link = get_dict_link(name, kanji, item_list)
    contents.append(dict_link)

  dict_body = {
    "type": "box",
    "layout": "vertical",
    "background": {
      "type": "linearGradient",
      "angle": "0deg",
      "startColor": "#ff8888",
      "endColor": "#ffffff"},
    "contents": contents
   }
  return dict_body


def get_result(name, score, item_list, isRanking):
  dict_body = get_dict_body(name, score, item_list, isRanking, 0)    
  payload = {
    "type": "flex",
    "altText": "Flex Message",
    "contents": {
      "type": "bubble",
      "body": dict_body
    }
  }
  return payload

def get_results(results, isRanking):
  dict_bodies = []    
  for i, result in enumerate(results):
    dict_body = get_dict_body(result["uname"], result["kanji"], result["table"], isRanking, i)
    dict_bodies.append(dict_body)
  payload = {
    "type": "flex",
    "altText": "Flex Message",
    "contents": {
      "type": "carousel",
      "contents": [
        {"type": "bubble", "body": dict_bodies[0]},
        {"type": "bubble", "body": dict_bodies[1]},
        {"type": "bubble", "body": dict_bodies[2]},
        {"type": "bubble", "body": dict_bodies[3]},
        {"type": "bubble", "body": dict_bodies[4]}
      ]
    }}
  return payload      

def noItems():
  payload = {
    "type": "flex",
    "altText": "Flex Message",
    "contents":{
      "type": "bubble",
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [{
          "type": "text",
          "text": "残念、品切れです。",
          "weight": "regular",
          "size": "md"},{
          "type": "text",
          "text": "0時になるとリセットされます。",
          "size": "md"}],
        "background": {
          "type": "linearGradient",
          "angle": "0deg",
          "startColor": "#ff8888",
          "endColor": "#ffffff"}}}}
  return payload


def kessan():
  payload = {
    "type": "flex",
    "altText": "Flex Message",
    "contents":{
      "type": "bubble",
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [{
          "type": "text",
          "text": "残念、未実装です。",
          "weight": "regular",
          "size": "md"},{
          "type": "text",
          "text": "しばらくお待ちください",
          "size": "md"}],
        "background": {
          "type": "linearGradient",
          "angle": "0deg",
          "startColor": "#ff8888",
          "endColor": "#ffffff"}}}}
  return payload


def elsemsg():
  payload = {
    "type": "flex",
    "altText": "Flex Message",
    "contents":{
      "type": "bubble",
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [{
          "type": "text",
          "text": "ごめん、意味わかんない。",
          "weight": "regular",
          "size": "md"}],
        "background": {
          "type": "linearGradient",
          "angle": "0deg",
          "startColor": "#ff8888",
          "endColor": "#ffffff"}}}}
  return payload