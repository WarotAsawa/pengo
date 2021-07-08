import os
import math

from linebot.models import (
    TextSendMessage, QuickReplyButton, MessageAction , TemplateSendMessage, CarouselTemplate, CarouselColumn, QuickReply
)
from AllResponse import AllResponse
from CSVOpener import CSVOpener
from LineConst import LineConst
from ImageConst import ImageConst

class Spec:

    #Generate Spec Reply String
    @staticmethod
    def GenerateSpecAnswers(specList, selectedProduct, selectedModel):
        fieldList = specList[0];
        unitList = specList[1];
        index = 0;
        #Prepare string response
        response = AllResponse.GetRandomResponseFromKeys('preAnswer') + "\n"
        response = response + "Here is the Spec of : " + selectedProduct + " " + selectedModel

        for i in range(2,len(specList)):
            model = specList[i][0]
            if selectedModel == model:
                index = i
                break
        if i==0: return TextSendMessage(text=AllResponse.GetRandomResponseFromKeys('errorWord'))
        buttonList = [];
        for i in range(1,len(fieldList)):
            fieldWhited = fieldList[i].replace("-", " ")
            response = response + "\n" + fieldWhited
            response = response + " : "
            response = response + str(specList[index][i]) + " " + unitList[i]
            lookupText = "lookup " + selectedProduct + " " + fieldList[i] + " " + str(specList[index][i])
            buttonList.append(QuickReplyButton(image_url=ImageConst.lookupIcon, action=MessageAction(label=fieldWhited[0:12], text=lookupText)))
        quickReply=QuickReply(items=buttonList)
        return TextSendMessage(text=response, quick_reply = quickReply);
    
    #Generate spec output
    @staticmethod
    def GenerateSpec(words):
        fileList = os.listdir(CSVOpener.csvPath)
        productList = [];
        modelList = [];
        specList = [];
        selectedProduct = ""
        selectedModel = ""
        #Get All Product Name from Directory
        for file in fileList:
            name = file.split('.')
            productList.append(name[0])
        #Check if Product name is valide and output error
        if (len(words) > 1):
            errorMessage = AllResponse.GetRandomResponseFromKeys("errorWord") + "\nPlease type \"spec\" or Select one of these product:\n"
            for product in productList:
                errorMessage = errorMessage + "\n - " + product;
                if words[1] == product.strip().lower():
                    selectedProduct = product
            #If No matched product, return Error Message Else got Model List
            if selectedProduct == "":
                return [TextSendMessage(text=errorMessage)]

            #Get Product's Model List
            specList = CSVOpener.GetArrayFromCSV(CSVOpener.csvPath+selectedProduct+".csv")
            for i in range(2,len(specList)):
                model = str(specList[i][0])
                modelList.append(model)
                
        #Check if Model name is valide and output error
        if (len(words) > 2):
            errorMessage = AllResponse.GetRandomResponseFromKeys("errorWord") + "\nPlease type \"spec " + selectedProduct + "\" or Select one of these model:\n"
            for model in modelList:
                errorMessage = errorMessage + model + " "
                if words[2] == model.strip().lower():
                    selectedModel = model
            #If No matched model, return Error Message Else got Model List
            if selectedModel == "":
                return [TextSendMessage(text=errorMessage)]
        
        #Set Column and Item Limit
        maxAction = LineConst.maxCarouselColumn * LineConst.maxActionPerColumn
        #Create Carosel Colume base on product or Model
        columnList = []
        loopList = []
        textPreFix = ""
        title = ""
        #Check if command is completed
        if selectedProduct != "" and selectedModel != "":
            specResponse = Spec.GenerateSpecAnswers(specList, selectedProduct, selectedModel)
            return specResponse
        #check command's len to prepare return message
        if (len(words) == 2):
            loopList = modelList
            textPreFix = "spec " + selectedProduct + " "
            title = "Choose Your Model"
        elif (len(words) == 1):
            loopList = productList
            textPreFix = "spec "
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
            columnList.append(CarouselColumn(text='Page '+str(i+1), title=title, actions=actions))
        carousel_template = CarouselTemplate(columns=columnList)

        specMessage = TemplateSendMessage(
            alt_text='Spec Wizard support only on Mobile',
            template=carousel_template
        )
        return specMessage
