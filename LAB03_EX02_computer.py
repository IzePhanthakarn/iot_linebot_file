from flask import Flask, request
from linebot import LineBotApi, WebhookHandler
from linebot.models import MessageEvent, TextMessage,TextSendMessage

import paho.mqtt.client as mqttClient
import time

channel_secret = "3389a655d713132847ebaa9bdbd66aec"
channel_access_token = "NNC0gDgUnkg8mgnh+V75LhYNAb9Gw5k/WXLxoHkoDbQbQ/TJMeC7Tpc3BvZQSKOcwH7E4bQ+Xg2rRGZQ8tfqZ128O8C0giBprLpCF89Q/s4jw2+fB9jVH+OZTjn8UkLmeHTr6pQgfmKH72WsT4LLHAdB04t89/1O/w1cDnyilFU="

broker_address= "mqtt.netpie.io"
port = 1883

client = mqttClient.Client("2334f5ea-bd2e-4c4c-8f75-1996a41c8358") # Client ID
user = "ByJgtZJcWSSAHB3Qph6zGASsD2tzDeZS" # Token
password = "qH~ctll8KUt80a87j0tb*m8Zq~X0MRS0" # Secret              
client.username_pw_set(user, password=password)    

try:
    client.connect(broker_address, port=port)        
except:
    print("Connection failed")

line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)

app = Flask(__name__)

@app.route("/", methods=["GET","POST"])
def home():
    try:
        signature = request.headers["X-Line-Signature"]
        body = request.get_data(as_text=True)
        handler.handle(body, signature)
    except:
        pass
    
    return "Hello Line Chatbot"

@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    #global temp,humi
    text = event.message.text
    print(text)    
    
    if (text=="เปิดไฟ"):
        client.publish("@msg/led","ledon")
        text_out = "เปิดไฟเรียบร้อยแล้ว"
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=text_out))

    if (text=="ปิดไฟ"):
        client.publish("@msg/led","ledoff")
        text_out = "ปิดไฟเรียบร้อยแล้ว"
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=text_out))
                     
if __name__ == "__main__":          
    app.run()

