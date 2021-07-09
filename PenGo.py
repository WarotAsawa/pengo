import random
import sys, os
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, StickerMessage, ImageMessage, VideoMessage, AudioMessage
)
sys.path.insert(0, './pengo')
from GetResponse import GetResponse
from LineConst import LineConst

app = Flask(__name__)

line_bot_api = LineBotApi(LineConst.pengoAccessToken)
handler = WebhookHandler(LineConst.pengoSecret)

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
    profile = line_bot_api.get_profile(event.source.user_id)
    GetResponse.SendByInput(line_bot_api, event.reply_token, event.message.text, profile)
    #line_bot_api.reply_message(event.reply_token,TextSendMessage(text=event.message.text))

@handler.add(MessageEvent, message=StickerMessage)
def handle_sticker_message(event):
    profile = line_bot_api.get_profile(event.source.user_id)
    GetResponse.ReplySticker(line_bot_api, event.reply_token, profile)
    #StickerSendMessage(package_id=event.message.package_id,sticker_id=event.message.sticker_id)


@handler.add(MessageEvent, message=ImageMessage)
def handle_sticker_message(event):
    profile = line_bot_api.get_profile(event.source.user_id)
    GetResponse.ReplyImage(line_bot_api, event.reply_token, profile)
    #StickerSendMessage(package_id=event.message.package_id,sticker_id=event.message.sticker_id)


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)