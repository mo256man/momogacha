def get_payload(name, score, item_list):
    payload = {
        "type": "flex",
        "altText": "Flex Message",
        "contents": {
  "type": "bubble",
  "body": {
    "type": "box",
    "layout": "vertical",
    "background": {
      "type": "linearGradient",
      "angle": "0deg",
      "startColor": "#ff8888",
      "endColor": "#ffff00"},
    "contents": [
      {
        "type": "text",
        "text": name+"社長",
        "weight": "bold",
        "size": "xl"
      },
      {
        "type": "text",
        "text": score + "円",
        "wrap": True,
        "align": "end",
        "size": "lg",
        "color": "#000000",
        "weight": "bold"
      },
      {
        "type": "separator",
        "margin": "md",
        "color": "#808080"
      },
      {
        "type": "box",
        "layout": "vertical",
        "margin": "xxl",
        "spacing": "sm",
        "contents": [
          {
            "type": "box",
            "layout": "horizontal",
            "contents": [
              {
                "type": "text",
                "text": item_list[0][2],
                "color": "#111111",
                "flex": 0,
                "size": "lg"
              }
            ]
          },
          {
            "type": "box",
            "layout": "horizontal",
            "contents": [
              {
                "type": "text",
                "text": f"{item_list[0][0]}（{item_list[0][1]}）",
                "size": "md",
                "color": "#111111",
                "flex": 0
              },
              {
                "type": "text",
                "text": item_list[0][3],
                "size": "md",
                "color": "#111111",
                "align": "end"
              }
            ]
          }
        ]
      },
      {
        "type": "box",
        "layout": "vertical",
        "margin": "xxl",
        "spacing": "sm",
        "contents": [
          {
            "type": "box",
            "layout": "horizontal",
            "contents": [
              {
                "type": "text",
                "text": item_list[1][2],
                "color": "#111111",
                "flex": 0,
                "size": "lg"
              }
            ]
          },
          {
            "type": "box",
            "layout": "horizontal",
            "contents": [
              {
                "type": "text",
                "text": f"{item_list[1][0]}（{item_list[1][1]}）",
                "size": "md",
                "color": "#111111",
                "flex": 0
              },
              {
                "type": "text",
                "text": item_list[1][3],
                "size": "md",
                "color": "#111111",
                "align": "end"
              }
            ]
          }
        ]
      },
      {
        "type": "box",
        "layout": "vertical",
        "margin": "xxl",
        "spacing": "sm",
        "contents": [
          {
            "type": "box",
            "layout": "horizontal",
            "contents": [
              {
                "type": "text",
                "text": item_list[2][2],
                "color": "#111111",
                "flex": 0,
                "size": "lg"
              }
            ]
          },
          {
            "type": "box",
            "layout": "horizontal",
            "contents": [
              {
                "type": "text",
                "text": f"{item_list[2][0]}（{item_list[2][1]}）",
                "size": "md",
                "color": "#111111",
                "flex": 0
              },
              {
                "type": "text",
                "text": item_list[2][3],
                "size": "md",
                "color": "#111111",
                "align": "end"
              }
            ]
          }
        ]
      },
      {
        "type": "separator",
        "margin": "md",
        "color": "#808080"
      },
      {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "box",
            "layout": "horizontal",
            "contents": [
              {
                "type": "text",
                "text": "決算",
                "color": "#FF0000",
                "size": "lg"
              },
              {
                "type": "text",
                "text": "1位／全100件",
                "color": "#000000",
                "align": "end",
                "size": "lg"
              }
            ]
          }
        ],
        "margin": "lg"
      }
    ]
  }
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
          "endColor": "#ffff00"}}}}
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
          "endColor": "#ffff00"}}}}
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
          "endColor": "#ffff00"}}}}
  return payload