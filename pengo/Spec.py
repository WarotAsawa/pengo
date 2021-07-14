import os
import math

from linebot.models.flex_message import BoxComponent, BubbleContainer, FlexSendMessage, TextComponent

from linebot.models import (
    TextSendMessage, QuickReplyButton, MessageAction , TemplateSendMessage, CarouselTemplate, CarouselColumn, QuickReply
)
from AllResponse import AllResponse
from CSVOpener import CSVOpener
from LineConst import LineConst
from ImageConst import ImageConst
from Help import Help

class Spec:

    @staticmethod   
    def AddField(field):
        contents = []
        contents.append(TextComponent(text=field,color='#ff5964',size='sm',flex=11, wrap=True, weight='bold'))
        contents.append(TextComponent(text=' ',color='#666666',size='sm',flex=1, wrap=True))
        box = BoxComponent(layout='baseline',spacing='sm',contents=contents, margin='xl')
        return box

    @staticmethod   
    def AddValue(value):
        contents = []
        contents.append(TextComponent(text=' ',color='#ff5964',size='sm',flex=1, wrap=True, weight='bold'))
        contents.append(TextComponent(text=value,color='#666666',size='sm',flex=11, wrap=True))
        box = BoxComponent(layout='baseline',spacing='sm',contents=contents, margin='xs')
        return box

    #Generate Spec Reply String
    @staticmethod
    def GenerateSpecAnswers(specList, selectedProduct, selectedModel):
        fieldList = specList[0];
        unitList = specList[1];
        index = 0;
        #Prepare string response
        preAnswer = AllResponse.GetRandomResponseFromKeys('preAnswer')
        header = "Here is the Spec of : " + selectedProduct + " " + selectedModel
        postAnswer = "You can lookup these field below"
        #Add FLex Content
        contents = []
        headerContents = []
        #Add Header
        headerContents.append(TextComponent(text='Specification Result', weight='bold', size='xl'))
        contents.append(TextComponent(text=header, weight='bold', size='sm', margin='md'))

        for i in range(2,len(specList)):
            model = specList[i][0]
            if selectedModel == model:
                index = i
                break
        if i==0: return TextSendMessage(text=AllResponse.GetRandomResponseFromKeys('errorWord'))
        buttonList = []
        for i in range(1,len(fieldList)):
            fieldWhited = fieldList[i].replace("-", " ")
            contents.append(Spec.AddField(fieldWhited))
            valueString = str(specList[index][i]) + " " + unitList[i]
            contents.append(Spec.AddValue(valueString))
            lookupText = "lookup " + selectedProduct + " " + fieldList[i] + " " + str(specList[index][i])
            if (i <= LineConst.maxQuickReply):
                buttonList.append(QuickReplyButton(image_url=ImageConst.lookupIcon, action=MessageAction(label=fieldWhited[0:12], text=lookupText)))

        #Add Contents
        headerContents.append(BoxComponent(layout='vertical',margin='lg',spacing='sm', contents=contents))
        body = BoxComponent(layout='vertical', contents=headerContents)
        bubble = BubbleContainer(direction='ltr',body=body)
        #Return Flex Message
        answer = FlexSendMessage(alt_text="Spec Results", contents=bubble)

        quickReply=QuickReply(items=buttonList)

        return [TextSendMessage(text=preAnswer), answer, TextSendMessage(text=postAnswer, quick_reply=quickReply)]
    
    #Generate spec output
    @staticmethod
    def GenerateSpec(words):
        dirList = os.listdir(CSVOpener.csvPath)
        dirList.sort()
        productList = [];
        modelList = [];
        specList = [];
        selectedProduct = ""
        selectedModel = ""
        #Get All Product Name from Directory
        for dir in dirList:
            fileList = os.listdir(CSVOpener.csvPath+dir+'/')
            fileList.sort()
            for file in fileList:
                name = file.split('.')
                productList.append(name[0])
        #Check if Product name is valide and output error
        if (len(words) > 1):
            errorMessage = AllResponse.GetRandomResponseFromKeys("errorWord") + "\nYour Product was no found.\nPlease Select one of these Products:\n"
            for product in productList:
                errorMessage = errorMessage + "\n - " + product;
                if words[1] == product.strip().lower():
                    selectedProduct = product
            #If No matched product, return Error Message Else got Model List
            if selectedProduct == "":
                return [TextSendMessage(text=errorMessage), Help.GenerateCarousel(type="spec model", list = productList)]
            errorMessage += "\nOr select your 'Product' the carousel below."

            #Get Product's Model List
            specList = CSVOpener.SearchAndOpenCSV(selectedProduct)
            for i in range(2,len(specList)):
                model = str(specList[i][0])
                modelList.append(model)
                
        #Check if Model name is valide and output error
        if (len(words) > 2):
            errorMessage = AllResponse.GetRandomResponseFromKeys("errorWord") + "\nYour Model was no found.\nPlease Select one of these Model:\n"
            for model in modelList:
                #Prepare error message and quick reply buttons
                errorMessage = errorMessage + model + " "
                if words[2] == model.strip().lower():
                    selectedModel = model
            errorMessage += "\nOr select in your 'Model' the carousel below."

            #If No matched model, return Error Message Else got Model List
            if selectedModel == "":
                return [TextSendMessage(text=errorMessage), Help.GenerateCarousel(type="spec model", list = modelList, selectedProduct=selectedProduct)]
        
        #Check if command is completed
        if selectedProduct != "" and selectedModel != "":
            specResponse = Spec.GenerateSpecAnswers(specList, selectedProduct, selectedModel)
            return specResponse
        #check command's len to prepare return message
        if (len(words) == 2):
            return Help.GenerateCarousel(type="spec model", list = modelList, selectedProduct=selectedProduct)
        elif (len(words) == 1):
            return Help.GenerateCarousel(type="spec product", list = productList, selectedProduct=selectedProduct)
        