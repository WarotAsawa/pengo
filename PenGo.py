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

