from flask import Flask, request
from linebot import LineBotApi, WebhookHandler
from linebot.models import (MessageEvent,
                            TextMessage,
                            TextSendMessage,
                            FlexSendMessage,
                            BubbleContainer,
                            BoxComponent,
                            TextComponent,
                            BubbleStyle,
                            BlockStyle)

import paho.mqtt.client as mqttClient
import time

temp = ""
humi = ""

def on_message(client, userdata, msg):
    global temp,humi
    print(msg.topic+" "+str(msg.payload))
    text_t_h = msg.payload.decode('UTF-8') # "25,80"
    t_and_h = text_t_h.split(',') # "25,80" --> ["25","80"]
    temp = t_and_h[0] # "25"
    humi = t_and_h[1] # "80"

channel_secret = "3389a655d713132847ebaa9bdbd66aec"
channel_access_token = "NNC0gDgUnkg8mgnh+V75LhYNAb9Gw5k/WXLxoHkoDbQbQ/TJMeC7Tpc3BvZQSKOcwH7E4bQ+Xg2rRGZQ8tfqZ128O8C0giBprLpCF89Q/s4jw2+fB9jVH+OZTjn8UkLmeHTr6pQgfmKH72WsT4LLHAdB04t89/1O/w1cDnyilFU="

broker_address= "mqtt.netpie.io"
port = 1883

client = mqttClient.Client("2334f5ea-bd2e-4c4c-8f75-1996a41c8358") # Client ID
user = "ByJgtZJcWSSAHB3Qph6zGASsD2tzDeZS" # Token
password = "qH~ctll8KUt80a87j0tb*m8Zq~X0MRS0" # Secret               
client.username_pw_set(user, password=password)    
client.on_message = on_message

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
    global temp,humi
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

    if (text=="สีแดง"):
        client.publish("@msg/color","red")
        text_out = "เปิดไฟสีแดงเรียบร้อยแล้ว"
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=text_out))

    if (text=="สีเขียว"):
        client.publish("@msg/color","green")
        text_out = "เปิดไฟสีเขียวเรียบร้อยแล้ว"
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=text_out))

    if (text=="สีน้ำเงิน"):
        client.publish("@msg/color","blue")
        text_out = "เปิดไฟสีน้ำเงินเรียบร้อยแล้ว"
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=text_out))

    if (text=="อุณหภูมิและความชื้น"):
        client.subscribe("@msg/t_h")
        client.loop_start()
        time.sleep(1.5) 
        client.loop_stop()
        # "25" 2
        # "90" 2
        if len(temp) > 0 and len(humi) > 0:
            #text_out = "อุณหภูมิ " + temp + " ความชื้น " + humi
            #line_bot_api.reply_message(event.reply_token,TextSendMessage(text=text_out))
            flex = BubbleContainer(
                size = 'mega', # nano,micro,kilo,*mega,giga
                styles = BubbleStyle(body=BlockStyle(background_color='#d8facc')),
                body = BoxComponent(
                    layout='horizontal',
                    contents=[BoxComponent(layout='vertical',
                                           contents=[
                                               TextComponent(text='อุณหภูมิ',
                                                             align='center',
                                                             color='#000000',
                                                             weight='bold',
                                                             style='normal',
                                                             decoration='none',
                                                             size='xl'
                                                             ),
                                               TextComponent(text=temp,
                                                             align='center',
                                                             color='#416fec',
                                                             weight='bold',
                                                             style='normal', 
                                                             decoration='none', 
                                                             size='4xl' 
                                                              )]),
                              BoxComponent(layout='vertical',
                                           contents=[
                                               TextComponent(text='ความชื้น',
                                                             align='center',
                                                             color='#000000',
                                                             weight='bold',
                                                             style='normal',
                                                             decoration='none',
                                                             size='xl'
                                                             ),
                                               TextComponent(text=humi,
                                                             align='center',
                                                             color='#38761d',
                                                             weight='bold',
                                                             style='normal', 
                                                             decoration='none', 
                                                             size='4xl' 
                                                              )])]))        
            flex_message = FlexSendMessage(alt_text='Hello',contents=flex)
            line_bot_api.reply_message(event.reply_token,flex_message)

if __name__ == "__main__":          
    app.run()

