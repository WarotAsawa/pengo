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

app = Flask(__name__)

#Channel Credentials
pengoAccessToken = "gLXVTlAYUxh8Onl1495Wg+CeW2AUBqcSM9Sd3cpnyAMiyBoJKk5cLrgm2VVG3rkLyspyeC9QU6tti5dXMn4M3xqkILBQulRUp4DK3Yb+0Ur/doUaJdFtj1CyQU43CU133mwZm/mmL9uYYIWFlDE6nAdB04t89/1O/w1cDnyilFU="
pengoSecret = "13f2ec4cf3d917223750d76498323737"
line_bot_api = LineBotApi(pengoAccessToken)
handler = WebhookHandler(pengoSecret)

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
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)