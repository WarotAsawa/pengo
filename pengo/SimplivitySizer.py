import math
import random

from linebot.models import (
    TextSendMessage, QuickReplyButton, MessageAction , TemplateSendMessage, CarouselTemplate, CarouselColumn, QuickReply
)
from Converter import Converter
from LineConst import LineConst
from ImageConst import ImageConst
from AllResponse import AllResponse
from CSVOpener import CSVOpener
class SimplivitySizer:
    
    @staticmethod
    def GetSimplivityModel():
        model = []
        #Get From File
        modelMatrix = CSVOpener.GetArrayFromCSV(CSVOpener.csvPath+"Storage/Simplivity.csv")
        for i in range(2,len(modelMatrix)):
            model.append(str(modelMatrix[i][0]).upper().strip())
        return model

    @staticmethod
    def GetSimplivityUsableCapacity():
        model = []
        #Get From File
        modelMatrix = CSVOpener.GetArrayFromCSV(CSVOpener.csvPath+"Storage/Simplivity.csv")
        for i in range(2,len(modelMatrix)):
            try:
                capacity = float(modelMatrix[i][4])
            except ValueError:
                capacity = 0.001
            model.append(capacity)
        return model


    @staticmethod
    def GenerateSimplivitySizeAnswers(unit = "TB", required = 50.0, utilization = 100.0):
        multiplier = Converter.TBToUnitMultipler(unit)
        convertedRequired = required * multiplier * 100 / utilization
        result = AllResponse.GetRandomResponseFromKeys('preAnswer') + "\n"
        modelList = SimplivitySizer.GetSimplivityModel()
        modelCapacity = SimplivitySizer.GetSimplivityUsableCapacity()
        config = 0;
        for i in range(0,len(modelList)):
            TiBPerNode = modelCapacity[i]
            TBPerNode = modelCapacity[i] * Converter.TBToUnitMultipler("TiB")

            requiredNode = math.ceil(convertedRequired/TBPerNode)
            if requiredNode > 32: continue
            if requiredNode == 1: requiredNode = 2
            config += 1
            model = modelList[i]
            totalUsableTiB = round(requiredNode * TiBPerNode,2)
            totalUsableTB = round(requiredNode * TBPerNode,2)
            result += "------------------\n"
            result += model + ": " + str(requiredNode) + "xNodes\nUsable:" + str(totalUsableTB) + "TB/" + str(totalUsableTiB) + "TiB\n"

        buttonList = [];
        TB100 = "TB"
        TiB100 = "TiB"
        TB90 = "TB @70%"
        TiB90 = "TiB @70%"
        strSizing = str(math.floor(required))
        newRand = random.randint(10, 522)
        #Check if has no answers
        if config ==0:
            result = AllResponse.GetRandomResponseFromKeys('errorWord') + "\nYour Sizing is too big for 32-Node Simplivity !!\nTry these instead."
            strSizing = str(newRand)
            required = newRand

        buttonList.append(QuickReplyButton(image_url=ImageConst.sizeIcon, action=MessageAction(label=strSizing+TB100, text="size SimpliVity "+str(required)+" TB")))
        buttonList.append(QuickReplyButton(image_url=ImageConst.sizeIcon, action=MessageAction(label=strSizing+TiB100, text="size SimpliVity "+str(required)+" TiB")))
        buttonList.append(QuickReplyButton(image_url=ImageConst.sizeIcon, action=MessageAction(label=strSizing+TB90, text="size SimpliVity "+str(required)+" TB 70")))
        buttonList.append(QuickReplyButton(image_url=ImageConst.sizeIcon, action=MessageAction(label=strSizing+TiB90, text="size SimpliVity "+str(required)+" TiB 70")))

        quickReply=QuickReply(items=buttonList)

        return TextSendMessage(text=result, quick_reply=quickReply)
        #, quick_reply=quickReply)


    @staticmethod
    def GenerateExampleCarousel(warning):
        title = "SimpliVity Capacity Sizing with Model"
        textPreFix = "size SimpliVity "
        exampleList = ["10 TB", "20 TiB", "30 TB","40 TiB", "50 TB", "60 TiB"]
        columnList = []
        #Set Column and Item Limit
        maxAction = LineConst.maxCarouselColumn * LineConst.maxActionPerColumn
        #check command's len to prepare return message
        for i in range(int(math.ceil(len(exampleList)/LineConst.maxActionPerColumn))):
            if i >= LineConst.maxCarouselColumn: break
            actions = []
            for j in range(i*LineConst.maxActionPerColumn,(i*LineConst.maxActionPerColumn)+LineConst.maxActionPerColumn):
                if j >= maxAction: break
                if j >= len(exampleList):
                    actions.append(MessageAction(label=". . .",text=textPreFix))
                else:
                    actions.append(MessageAction(label=exampleList[j][0:12],text=textPreFix + exampleList[j]))
            columnList.append(CarouselColumn(thumbnail_image_url =ImageConst.sizeImage, text='Usage\nsize SimpliVity [required usable] [TB/TiB]', title=title, actions=actions))

        carousel_template = CarouselTemplate(columns=columnList)
        carousel = TemplateSendMessage(
            alt_text='Sizing Wizard support only on Mobile',
            template=carousel_template
        )
        return [TextSendMessage(text=warning), carousel]

    @staticmethod
    def GenerateSimplivitySizer(words):
        if len(words) == 2:
            return SimplivitySizer.GenerateExampleCarousel("SimpliVity Sizer Example")
        elif len(words) == 3:
            required = 0.0
            try:
                required = float(words[2])
            except ValueError:
                return SimplivitySizer.GenerateExampleCarousel("Please input capacity as Decimal") 
            
            return SimplivitySizer.GenerateSimplivitySizeAnswers(unit = "TB", required = required)
        elif len(words) > 3:
            required = 0.0
            #add utilization
            utilization = 100.0
            if len(words) > 4:
                try: utilization = float(words[4])
                except ValueError: utilization = 100.0
            if utilization <= 0: utilization = 1.0
            if utilization > 100: utilization = 100.0

            try:
                required = float(words[2])
            except ValueError:
                return SimplivitySizer.GenerateExampleCarousel("Please input capacity as float") 
            
            #Check if unit is tb or tib
            unit = words[3].lower()
            unitCheck = ["tb","tib"]
            #unitCheck = ["tb","tib", "gb", "gib", "pb", "pib"]
            if unit not in unitCheck:
                return SimplivitySizer.GenerateExampleCarousel("Please input unit as TB or TiB") 
            
            #Get Sizing
            return SimplivitySizer.GenerateSimplivitySizeAnswers(unit = unit, required = required, utilization = utilization)
