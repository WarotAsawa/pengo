import os
import math

from linebot.models import (
    TextSendMessage, QuickReplyButton, MessageAction , TemplateSendMessage, CarouselTemplate, CarouselColumn, QuickReply
)
from AllResponse import AllResponse
from CSVOpener import CSVOpener
from LineConst import LineConst
from ImageConst import ImageConst

class LookUp:

    #Generate Lookup Reply String
    @staticmethod
    def GenerateLookUpAnswers(specList, selectedProduct, fieldIndex, selectedValue):
        fieldList = specList[0]
        unitList = specList[1]
        count = 0
        #Prepare string response
        response = AllResponse.GetRandomResponseFromKeys('preAnswer') + "\n"
        response = response + "Here is the list of model of : " + selectedProduct + ", which " + fieldList[fieldIndex] + " is " + selectedValue + " " + unitList[fieldIndex];
        uniqueValue = []
        allMatchModel = []
        buttonList = []
        for i in range(2,len(specList)):
            value = str(specList[i][fieldIndex]).lower().strip()
            if selectedValue == value:
                response = response + "\n - " + str(specList[i][0])
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
        
        quickReply=QuickReply(items=buttonList)
        #Print Carousel follow with Tips and Quick Reply
        return TextSendMessage(text=response, quick_reply=quickReply)

    #Generate lookUp output
    @staticmethod
    def GenerateLookUp(words):
        fileList = os.listdir(CSVOpener.csvPath)
        productList = [];
        fieldList = [];
        specList = [];
        valueList = [];
        selectedProduct = ""
        selectedField = ""
        selectedValue = ""
        fieldIndex = 0
        #Get All Product Name from Directory
        for file in fileList:
            name = file.split('.')
            productList.append(name[0])
        #Check if Product name is valide and output error
        if (len(words) > 1):
            errorMessage = AllResponse.GetRandomResponseFromKeys("errorWord") + "\nPlease type \"lookUp\" or Select one of these product:\n"
            for product in productList:
                errorMessage = errorMessage + "\n - " + product;
                if words[1] == product.strip().lower():
                    selectedProduct = product
            #If No matched product, return Error Message Else got Model List
            if selectedProduct == "":
                return [TextSendMessage(text=errorMessage)]

            #Get Product's Field List
            specList = CSVOpener.GetArrayFromCSV(CSVOpener.csvPath+selectedProduct+".csv")
            for i in range(1,len(specList[0])):
                field = str(specList[0][i])
                fieldList.append(field)
                
        #Check if Field name is valide and output error
        if (len(words) > 2):
            errorMessage = AllResponse.GetRandomResponseFromKeys("errorWord") + "\nPlease type \"lookUp " + selectedProduct + "\" or Select one of these field:\n"
            for i in range(len(fieldList)):
                field = fieldList[i]
                errorMessage = errorMessage + field + " "
                if words[2] == field.strip().lower():
                    selectedField = field
                    fieldIndex = i+1

            #If No matched Field, return Error Message Else got Field List
            if selectedField == "":
                return [TextSendMessage(text=errorMessage)]

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
        #Set Column and Item Limit
        maxAction = LineConst.maxCarouselColumn * LineConst.maxActionPerColumn
        #Create Carosel Colume base on product or Model or Field
        columnList = []
        loopList = []
        textPreFix = ""
        title = ""
        #Check if command is completed
        if selectedProduct != "" and selectedField != "" and selectedValue != "":
            lookUpResponse = LookUp.GenerateLookUpAnswers(specList, selectedProduct, fieldIndex, selectedValue)
            return lookUpResponse
        #check command's len to prepare return message
        if (len(words) == 3):
            loopList = valueList
            textPreFix = "lookUp " + selectedProduct + " " + selectedField + " "
            title = "Choose Your Value"
        elif (len(words) == 2):
            loopList = fieldList
            textPreFix = "lookUp " + selectedProduct + " "
            title = "Choose Your Field"
        elif (len(words) == 1):
            loopList = productList
            textPreFix = "lookUp "
            title = "Choose Your Product"
        for i in range(int(math.ceil(len(loopList)/LineConst.maxActionPerColumn))):
            if i >= LineConst.maxCarouselColumn: break
            actions = []
            for j in range(i*LineConst.maxActionPerColumn,(i*LineConst.maxActionPerColumn)+LineConst.maxActionPerColumn):
                if j >= maxAction: break
                if j >= len(loopList):
                    actions.append(MessageAction(label=". . .",text=textPreFix))
                else:
                    actions.append(MessageAction(label=loopList[j][0:12],text=textPreFix + loopList[j]))
            columnList.append(CarouselColumn(thumbnail_image_url =ImageConst.lookupImage, text='Page '+str(i+1), title=title, actions=actions))
        carousel_template = CarouselTemplate(columns=columnList)

        lookUpMessage = TemplateSendMessage(
            alt_text='LookUp Wizard support only on Mobile',
            template=carousel_template
        )
        return lookUpMessage
