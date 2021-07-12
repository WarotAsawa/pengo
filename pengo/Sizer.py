import random;
import csv;
import os;
import math

from linebot.models.flex_message import BoxComponent, TextComponent
from ImageConst import ImageConst
from NimbleSizer import NimbleSizer;

from linebot import (
    LineBotApi
)
from linebot.models import (
    TextSendMessage, QuickReplyButton, MessageAction , TemplateSendMessage, CarouselTemplate, CarouselColumn, QuickReply
)
from LineConst import LineConst
from PrimeraSizer import PrimeraSizer
from SimplivitySizer import SimplivitySizer

class Sizer:

    #List Supported Product
    products = ["Primera", "Nimble", "SimpliVity"]
    @staticmethod
    def GetSizerMenu():
        title = "Select Your Product"
        textPreFix = "size "
        productList = Sizer.products
        columnList = []
        #Set Column and Item Limit
        maxAction = LineConst.maxCarouselColumn * LineConst.maxActionPerColumn
        #check command's len to prepare return message
        for i in range(int(math.ceil(len(productList)/LineConst.maxActionPerColumn))):
            if i >= LineConst.maxCarouselColumn: break
            actions = []
            for j in range(i*LineConst.maxActionPerColumn,(i*LineConst.maxActionPerColumn)+LineConst.maxActionPerColumn):
                if j >= maxAction: break
                if j >= len(productList):
                    actions.append(MessageAction(label=". . .",text=textPreFix))
                else:
                    actions.append(MessageAction(label=productList[j][0:12],text=textPreFix + productList[j]))
            columnList.append(CarouselColumn(thumbnail_image_url =ImageConst.sizeImage, text='Page '+str(i+1), title=title, actions=actions))
        carousel_template = CarouselTemplate(columns=columnList)

        specMessage = TemplateSendMessage(
            alt_text='Sizing Wizard support only on Mobile',
            template=carousel_template
        )

        return specMessage

    @staticmethod
    def GenerateSizerResponse(words):
        if len(words) == 1:
            return Sizer.GetSizerMenu()
        elif len(words) > 1:
            selectedProduct = str(words[1]).lower().strip()
            #Check if valid product
            unMatch = True
            for product in Sizer.products:
                if selectedProduct == product.lower().strip(): unMatch = False
            if unMatch: return [TextSendMessage(text="Please Select supported Products"),Sizer.GetSizerMenu()]
            if selectedProduct == "primera":
                return PrimeraSizer.GeneratePrimeraSizer(words)
            elif selectedProduct == "nimble":
                return NimbleSizer.GenerateNimbleSizer(words)
            elif selectedProduct == "simplivity":
                return SimplivitySizer.GenerateSimplivitySizer(words)