import random;
import csv;
import os;
import math;

from linebot import (
    LineBotApi
)
from linebot.models import (
    TextSendMessage, QuickReplyButton, MessageAction , TemplateSendMessage, CarouselTemplate, CarouselColumn, QuickReply
)
class Sizer:
    @staticmethod
    def GetSizerMenu():
        return ""