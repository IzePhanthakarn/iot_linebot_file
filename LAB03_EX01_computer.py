from flask import Flask, request
from linebot import LineBotApi, WebhookHandler
from linebot.models import MessageEvent, TextMessage

channel_secret = "3389a655d713132847ebaa9bdbd66aec" # หน้าบ้าน --> หลังบ้าน
channel_access_token = "NNC0gDgUnkg8mgnh+V75LhYNAb9Gw5k/WXLxoHkoDbQbQ/TJMeC7Tpc3BvZQSKOcwH7E4bQ+Xg2rRGZQ8tfqZ128O8C0giBprLpCF89Q/s4jw2+fB9jVH+OZTjn8UkLmeHTr6pQgfmKH72WsT4LLHAdB04t89/1O/w1cDnyilFU=" # หลังบ้าน --> หน้าบ้าน

line_bot_api = LineBotApi(channel_access_token) # หลังบ้าน --> หน้าบ้าน
handler = WebhookHandler(channel_secret)        # หน้าบ้าน --> หลังบ้าน

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
    text = event.message.text
    print(text)

if __name__ == "__main__":  
    app.run()


    

