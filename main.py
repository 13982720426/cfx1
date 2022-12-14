from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random

today = datetime.now()
start_date = os.environ['START_DATE']
city = os.environ['CITY']
birthday = os.environ['BIRTHDAY']
birthday2 = os.environ['BIRTHDAY2']

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

user_id = os.environ["USER_ID"]
user_id2 = os.environ["USER_ID2"]
template_id = os.environ["TEMPLATE_ID"]


def get_weather():
  url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city
  res = requests.get(url).json()
  weather = res['data']['list'][0]
  return weather['weather'], math.floor(weather['temp']), weather['lastUpdateTime'], math.floor(weather['low']), math.floor(weather['high']), weather['humidity'], weather['wind']

def get_count():
  delta = today - datetime.strptime(start_date, "%Y-%m-%d")
  return delta.days

def get_birthday():
  next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - today).days

def get_birthday2():
  next = datetime.strptime(str(date.today().year) + "-" + birthday2, "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - today).days

def get_words():
  words = requests.get("https://api.shadiao.pro/chp")
  if words.status_code != 200:
    return get_words()
  return words.json()['data']['text']

def get_random_color():
  return "#%06x" % random.randint(0, 0xFFFFFF)


client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)
wea, temperature, lastUpdateTime, low, high, humidity, wind = get_weather()
data = {
  "text":{
    "value":'今天也要加油呀！',
    "color":'#fe0000'
  },
  "city":{
    "value":city,
  },
  "weather":{
    "value":wea,
  },
  "low":{
    "value":low,
  },
  "high":{
    "value":high,
  },
  "wind":{
    "value":wind,
  },
  "temperature":{
    "value":temperature,
    "color":'#f73131'
  },
  "humidity":{
    "value":humidity,
    "color":'#278dff'
  },
  "lastUpdateTime":{
    "value":lastUpdateTime,
    "color":'#fb7555'
  },
  "love_days":{
    "value":get_count(),
    "color":'#fe0000'
  },
  "birthday_left":{
    "value":get_birthday(),
    "color":'#fe0000'
  },
  "birthday_left2":{
    "value":get_birthday2(),
    "color":'#fe0000'
  },
  "words":{
    "value":get_words(), 
    "color":get_random_color()
  }
}
res = wm.send_template(user_id, template_id, data)
res2 = wm.send_template(user_id2, template_id, data)
print(res)
print(res2)
