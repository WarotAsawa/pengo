import csv;
import os;
import math


from linebot import (
    LineBotApi
)
from linebot.models import (
    TextSendMessage, QuickReplyButton, MessageAction , TemplateSendMessage, CarouselTemplate, CarouselColumn, QuickReply
)
from AllResponse import AllResponse
from CSVOpener import CSVOpener
from LineConst import LineConst
from ImageConst import ImageConst
from Help import Help
from Spec import Spec
from LookUp import LookUp

class GetResponse:
    
    #Everything Start Here . Except Main
    @staticmethod
    def SendByInput(line_bot_api: LineBotApi,token, input):
        lowerInput = input.lower()
        trimmedInput = lowerInput.strip()
        words = str.split(trimmedInput)
        response = ""
        if "help" in words:
            if "spec" in words:
                response = AllResponse.allResponse["helpspec"]
            elif "lookup" in words:
                response = AllResponse.allResponse["helplookup"]
            else:
                line_bot_api.reply_message(token,Help.GenerateHelp())
                return
        elif "spec" in words:
            line_bot_api.reply_message(token,Spec.GenerateSpec(words))
        elif "lookup" in words:
            line_bot_api.reply_message(token,LookUp.GenerateLookUp(words))
        elif "hello" in words or "hi" in words or "greet" in words:
            response = AllResponse.GetRandomResponseFromKeys('hello')
        elif "thank" in words:
            response = AllResponse.GetRandomResponseFromKeys('thank')
        elif "bye" in words:
            response = AllResponse.GetRandomResponseFromKeys('bye')
        elif "why" in words:
            response = AllResponse.GetRandomResponseFromKeys('why')
        elif "when" in words:
            response = AllResponse.GetRandomResponseFromKeys('when')
        elif "where" in words:
            response = AllResponse.GetRandomResponseFromKeys('where')
        elif "how" in words:
            if "are" in words and "you" in words:
                response = AllResponse.allResponse["howareyou"]
            else:
                response = AllResponse.GetRandomResponseFromKeys('how')
        else:
            response = AllResponse.GetRandomResponseFromKeys('joke') + "\n\n" + AllResponse.GetRandomResponseFromKeys('helptips')

        line_bot_api.reply_message(token,TextSendMessage(text=response, quick_reply=Help.GeneralHelp()))
        return   