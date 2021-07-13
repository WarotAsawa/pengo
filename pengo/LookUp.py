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

class LookUp:

    @staticmethod   
    def AddHeader(title, value):
        contents = []
        contents.append(TextComponent(text=title,color='#666666',size='sm',flex=1, wrap=True, weight='bold'))
        contents.append(TextComponent(text=value,color='#00c0ff',size='sm',flex=3, wrap=True))
        box = BoxComponent(layout='baseline',spacing='sm',contents=contents, margin='sm')
        return box

    @staticmethod   
    def AddValue(value):
        contents = []
        contents.append(TextComponent(text=' ',color='#00c0ff',size='sm',flex=1, wrap=True, weight='bold'))
        contents.append(TextComponent(text=value,color='#666666',size='sm',flex=11, wrap=True))
        box = BoxComponent(layout='baseline',spacing='sm',contents=contents, margin='xs')
        return box

    #Generate Lookup Reply String
    @staticmethod
    def GenerateLookUpAnswers(specList, selectedProduct, fieldIndex, selectedValue):
        fieldList = specList[0]
        unitList = specList[1]
        count = 0
        #Prepare string response
        preAnswer = AllResponse.GetRandomResponseFromKeys('preAnswer')
        header = "This is what you want to find"
        postAnswer = "You can lookup these field below"
        #Add FLex Content
        contents = []
        headerContents = []
        #Add Header
        headerContents.append(TextComponent(text='Look Up Result', weight='bold', size='xl'))
        contents.append(TextComponent(text=header, weight='bold', size='sm', margin='md'))
        contents.append(LookUp.AddHeader("Field", fieldList[fieldIndex]))
        contents.append(LookUp.AddHeader("Value", selectedValue + " " + unitList[fieldIndex]))
        header = "Here is the matched " + selectedProduct + " model!"
        contents.append(TextComponent(text=header, weight='bold', size='sm', margin='xl'))
        #Prepare string response
        uniqueValue = []
        allMatchModel = []
        buttonList = []
        for i in range(2,len(specList)):
            value = str(specList[i][fieldIndex]).lower().strip()
            if selectedValue == value:
                contents.append(LookUp.AddValue(str(specList[i][0])))
                allMatchModel.append(str(specList[i][0]))
                count = count + 1
            if value not in uniqueValue:
                uniqueValue.append(value)

        #Add quickreply for spec for match model
        for i in range(len(allMatchModel)):
            if i >= LineConst.maxQuickReply: break
            specText = "spec " + selectedProduct + " " + allMatchModel[i]
            buttonList.append(QuickReplyButton(image_url=ImageConst.specIcon, action=MessageAction(label=allMatchModel[i], text=specText)))

        if count == 0:
            response = AllResponse.GetRandomResponseFromKeys('errorWord') + "\n"
            response = response + "Cannot find any model of : " + selectedProduct + ", which " + fieldList[fieldIndex] + " is " + selectedValue + " " + unitList[fieldIndex];
            #Add quickreply for lookup for other value
            buttonList = []
            for i in range(len(uniqueValue)):
                if i >= LineConst.maxQuickReply: break
                lookupText = "lookup " + selectedProduct + " " + fieldList[fieldIndex] + " " + uniqueValue[i]
                buttonList.append(QuickReplyButton(image_url=ImageConst.lookupIcon, action=MessageAction(label=uniqueValue[i][0:20], text=lookupText)))
        
        #Add Contents
        headerContents.append(BoxComponent(layout='vertical',margin='lg',spacing='sm', contents=contents))
        body = BoxComponent(layout='vertical', contents=headerContents)
        bubble = BubbleContainer(direction='ltr',body=body)
        #Return Flex Message
        answer = FlexSendMessage(alt_text="Spec Results", contents=bubble)

        quickReply=QuickReply(items=buttonList)

        return [TextSendMessage(text=preAnswer), answer, TextSendMessage(text=postAnswer, quick_reply=quickReply)]

    #Generate lookUp output
    @staticmethod
    def GenerateLookUp(words):
        dirList = os.listdir(CSVOpener.csvPath)
        dirList.sort()
        productList = [];
        fieldList = [];
        specList = [];
        valueList = [];
        selectedProduct = ""
        selectedField = ""
        selectedValue = ""
        fieldIndex = 0
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
            errorMessage += "\nOr select your 'Product' the carousel below."
            #If No matched product, return Error Message Else got Model List
            if selectedProduct == "":
                return [TextSendMessage(text=errorMessage), Help.GenerateCarousel(type="lookup field", list = productList)]

            #Get Product's Field List
            specList = CSVOpener.SearchAndOpenCSV(selectedProduct)
            for i in range(1,len(specList[0])):
                field = str(specList[0][i])
                fieldList.append(field)
                
        #Check if Field name is valide and output error
        if (len(words) > 2):
            errorMessage = AllResponse.GetRandomResponseFromKeys("errorWord") + "\nYour Field was no found.\nPlease Select one of these Fields:\n"
            for i in range(len(fieldList)):
                field = fieldList[i]
                errorMessage = errorMessage + field + " "
                if words[2] == field.strip().lower():
                    selectedField = field
                    fieldIndex = i+1
            errorMessage += "\nOr select in your 'Field' the carousel below."

            #If No matched Field, return Error Message Else got Field List
            if selectedField == "":
                return [TextSendMessage(text=errorMessage), Help.GenerateCarousel(type="lookup field", list = fieldList, selectedProduct=selectedProduct)]

            #Get Field's Value List
            for i in range(2,len(specList)):
                value = str(specList[i][fieldIndex]).strip().lower()
                if value not in valueList:
                    valueList.append(value)
        
        #Check if input already field's value
        if (len(words) > 3):
            for i in range(3,len(words)):
                selectedValue = selectedValue + words[i] + " "
            selectedValue = selectedValue.strip().lower()
        
        #Check if command is completed
        if selectedProduct != "" and selectedField != "" and selectedValue != "":
            lookUpResponse = LookUp.GenerateLookUpAnswers(specList, selectedProduct, fieldIndex, selectedValue)
            return lookUpResponse
        #check command's len to prepare return message
        if (len(words) == 3):
            return Help.GenerateCarousel(type="lookup value", list = valueList, selectedProduct=selectedProduct, selectedField=selectedField)
        elif (len(words) == 2):
            return Help.GenerateCarousel(type="lookup field", list = fieldList, selectedProduct=selectedProduct)
        elif (len(words) == 1):
            return Help.GenerateCarousel(type="lookup field", list = productList)
