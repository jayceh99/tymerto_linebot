from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)
import os
import xml.dom.minidom
import get_all_train
app = Flask(__name__)

path = r'config.xml'
element = xml.dom.minidom.parse(path)

root = element.documentElement
channel_secret =  root.getElementsByTagName('channel_secret')[0].firstChild.data
channel_access_token =  root.getElementsByTagName('channel_access_token')[0].firstChild.data



line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    input_text = event.message.text
    if '?' in input_text:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='請輸入 起點,終點,時間 (使用,分開)\ne.g.\nA8,高鐵,!1400\n表示A8長庚醫院站到A18桃園高鐵站且"出發時間"為14點整\nA8,高鐵,@1400\n表示A8長庚醫院站到A18桃園高鐵站且"抵達時間"為14點整'))
    else:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=get_all_train.main(input_text)))
        




if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)