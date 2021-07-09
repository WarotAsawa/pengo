from linebot import (
    LineBotApi
)
from linebot.models import (
    TextSendMessage, StickerSendMessage
)
import random

from AllResponse import AllResponse
from CSVOpener import CSVOpener
from LineConst import LineConst
from ImageConst import ImageConst
from Help import Help
from Spec import Spec
from LookUp import LookUp
from Sizer import Sizer

class GetResponse:
    
    #Everything Start Here . Except Main
    @staticmethod
    def ReplySticker(line_bot_api: LineBotApi,token, input, profile):
        response = AllResponse.GetRandomResponseFromKeys('image')
        line_bot_api.reply_message(token,TextSendMessage(text=response, quick_reply=Help.GeneralHelp()))

    @staticmethod
    def ReplyImage(line_bot_api: LineBotApi,token, input, profile):
        line_bot_api.reply_message(token,StickerSendMessage(package_id=789,sticker_id=random.randrange(10855,10894)))

    @staticmethod
    def SendByInput(line_bot_api: LineBotApi,token, input, profile):
        userName = profile.display_name
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
        elif "size" in words:
            line_bot_api.reply_message(token,Sizer.GenerateSizerResponse(words))
        elif "hello" in words or "hi" in words or "greet" in words:
            response = AllResponse.GetRandomResponseFromKeys('hello') + " " + userName
        elif "thank" in words:
            response = AllResponse.GetRandomResponseFromKeys('thank') + " " + userName
        elif "bye" in words:
            response = AllResponse.GetRandomResponseFromKeys('bye') + " " + userName
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