import math
import random

from linebot.models.flex_message import BoxComponent, BubbleContainer, ButtonComponent, FlexSendMessage, ImageComponent, SeparatorComponent, TextComponent

from linebot.models import (
    TextSendMessage, QuickReplyButton, MessageAction , TemplateSendMessage, CarouselTemplate, CarouselColumn, QuickReply
)
from Converter import Converter
from Help import Help
from LineConst import LineConst
from ImageConst import ImageConst
from AllResponse import AllResponse
from CSVOpener import CSVOpener

class SimplivitySizer:

    @staticmethod   
    def AddModelRow(model, node):
        contents = []
        contents.append(TextComponent(text=model,color='#666666',size='md',flex=6, wrap=True, weight='bold'))
        contents.append(TextComponent(text=node,color='#00b088',size='md',flex=2, wrap=True, weight='bold', align='end'))
        contents.append(TextComponent(text="Nodes",color='#666666',size='md',flex=3, wrap=True, weight='regular', align='start'))
        box = BoxComponent(layout='baseline',spacing='sm',contents=contents, margin='xl')
        return box

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
        preAnswer = AllResponse.GetRandomResponseFromKeys('preAnswer')
        answer = TextSendMessage(text='Temp')
        postAnswer = "See below similar Sizings"
        modelList = SimplivitySizer.GetSimplivityModel()
        modelCapacity = SimplivitySizer.GetSimplivityUsableCapacity()

        #Add FLex Content
        contents = []
        headerContents = []
        #Add Header
        headerContents.append(TextComponent(text='Sizing Result', weight='bold', size='xl'))

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
            usableString = str(totalUsableTB) + "TB / " + str(totalUsableTiB) + "TiB"
            contents.append(SimplivitySizer.AddModelRow(model,str(requiredNode)))      
            contents.append(Help.AddFlexRow("Total Usable",usableString,3,6, weight='bold'))       
        #Check is OK
        if config == 0: contents = [TextComponent(text='Your Sizing is loo large for 32-Node SimpliVity', weight='bold', size='xl', color='#ff0000')]
        #Add Contents
        headerContents.append(BoxComponent(layout='vertical',margin='lg',spacing='sm', contents=contents))
        body = BoxComponent(layout='vertical', contents=headerContents)
        bubble = BubbleContainer(direction='ltr',body=body)
        #Return Flex Message
        answer = FlexSendMessage(alt_text="Nimble HF Sizing Results", contents=bubble)

        buttonList = [];
        TB100 = "TB"
        TiB100 = "TiB"
        TB90 = "TB @70%"
        TiB90 = "TiB @70%"
        strSizing = str(math.floor(required))
        newRand = random.randint(10, 522)
        #Check if has no answers
        if config ==0:
            preAnswer = AllResponse.GetRandomResponseFromKeys('errorWord')
            postAnswer = "No answers found !! Try these instead."
            strSizing = str(newRand)
            required = newRand

        buttonList.append(QuickReplyButton(image_url=ImageConst.sizeIcon, action=MessageAction(label=strSizing+TB100, text="size SimpliVity "+str(required)+" TB")))
        buttonList.append(QuickReplyButton(image_url=ImageConst.sizeIcon, action=MessageAction(label=strSizing+TiB100, text="size SimpliVity "+str(required)+" TiB")))
        buttonList.append(QuickReplyButton(image_url=ImageConst.sizeIcon, action=MessageAction(label=strSizing+TB90, text="size SimpliVity "+str(required)+" TB 70")))
        buttonList.append(QuickReplyButton(image_url=ImageConst.sizeIcon, action=MessageAction(label=strSizing+TiB90, text="size SimpliVity "+str(required)+" TiB 70")))

        quickReply=QuickReply(items=buttonList)

        return [TextSendMessage(text=preAnswer), answer, TextSendMessage(text=postAnswer, quick_reply=quickReply)]
        #, quick_reply=quickReply)


    @staticmethod
    def GenerateExampleCarousel(warning, capacity = 0):
        title = "Simplivity capacity sizing by model"
        exampleList = []
        textPreFix = "size simplivity "
        #If no capacity generate random units
        if capacity == 0:
            for i in range(0,10):
                unitRand = random.choice([" TB", " TiB"])
                capaRand = str(random.randint(1,25)*10)
                exampleList.append(capaRand+unitRand)
        else:
            #Is have capacity recommend units
            exampleList = [str(capacity)+" TB", str(capacity)+" TiB"]

        #Add FLex Content
        contents = []
        headerContents = []
        #Add Header
        headerContents.append(TextComponent(text=title, weight='bold', size='md',wrap=True))
        contents.append(TextComponent(text="Tip: size simplivity [required usable] [TB/TiB]", size='xs', wrap=True))
        #Add Model Button
        for i in range(0,math.floor(len(exampleList)/2)):
            buttonList = []
            buttonList.append(Help.DefaultButton(label=exampleList[i*2], text=textPreFix + exampleList[i*2]))
            buttonList.append(SeparatorComponent(margin='md'))
            buttonList.append(Help.DefaultButton(label=exampleList[i*2+1], text=textPreFix + exampleList[i*2+1]))
            box = BoxComponent(layout='horizontal',spacing='sm',contents=buttonList)
            contents.append(box)
        
        headerContents.append(BoxComponent(layout='vertical',margin='lg',spacing='sm', contents=contents))
        body = BoxComponent(layout='vertical', contents=headerContents)
        hero = ImageComponent(url=ImageConst.sizeImage,background_color=ImageConst.sizeColor,aspect_ratio='20:5',aspect_mode='fit',size='full')
        bubble = BubbleContainer(direction='ltr',body=body,hero=hero)
        bubbleMessage = FlexSendMessage(alt_text="Simplivity Sizing Example", contents=bubble)

        return [TextSendMessage(text=warning), bubbleMessage]
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
                return SimplivitySizer.GenerateExampleCarousel("Please input unit as TB or TiB", capacity=required) 
            
            #Get Sizing
            return SimplivitySizer.GenerateSimplivitySizeAnswers(unit = unit, required = required, utilization = utilization)
