import csv;
import os;
import math;

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

class GetResponse:
    
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
        for i in range(1,len(fieldList)):
            response = response + "\n" + fieldList[i].replace("-", " ")
            response = response + " : "
            response = response + str(specList[index][i]) + " " + unitList[i]
        return TextSendMessage(text=response);
    
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
                buttonList.append(QuickReplyButton(image_url=ImageConst.lookupIcon, action=MessageAction(label=uniqueValue[i], text=lookupText)))
        
        quickReply=QuickReply(items=buttonList)
        #Print Carousel follow with Tips and Quick Reply
        return TextSendMessage(text=response, quick_reply=quickReply)

    #Generate help output
    @staticmethod
    def GenerateHelp():
        #Spec Help Menu
        specTitle = 'spec :Show detail of product\'s model'
        specText = 'Tip: spec [product] [model]\nOr tab below to start'
        specAction = []
        specAction.append(MessageAction(label="spec",text='spec'))
        specAction.append(MessageAction(label="spec nimble",text='spec nimble'))
        specAction.append(MessageAction(label="spec rome 7262",text='spec rome 7262'))
        #Lookup Help Menu
        lookUpTitle = 'lookup :Search product\'s model by spec'
        lookUpText = 'Tip: lookup [product] [spec] [value]\nOr tab below to start'
        lookUpAction = []
        lookUpAction.append(MessageAction(label="lookup",text='lookup'))
        lookUpAction.append(MessageAction(label="lookup milan",text='lookup milan'))
        lookUpAction.append(MessageAction(label="lookup rome core 64",text='lookup rome core 64'))
        # Create Column List for Carosel
        columnList = []
        columnList.append(CarouselColumn(thumbnail_image_url =ImageConst.specImage, title=specTitle, text=specText, actions=specAction))
        columnList.append(CarouselColumn(thumbnail_image_url =ImageConst.lookupImage, title=lookUpTitle, text=lookUpText, actions=lookUpAction))
        carousel_template = CarouselTemplate(columns=columnList)
        helpCarousel = TemplateSendMessage(
            alt_text='Help Wizard support only on Mobile',
            template=carousel_template
        )
        #Create QuickReply ButtonList
        
        buttonList = [];
        buttonList.append(QuickReplyButton(image_url=ImageConst.specIcon, action=MessageAction(label="spec", text="spec")))
        buttonList.append(QuickReplyButton(image_url=ImageConst.specIcon, action=MessageAction(label="spec nimble", text="spec nimble")))
        buttonList.append(QuickReplyButton(image_url=ImageConst.specIcon, action=MessageAction(label="spec primera A630", text="spec primera A630")))
        buttonList.append(QuickReplyButton(image_url=ImageConst.specIcon, action=MessageAction(label="spec rome 7262 ", text="spec rome 7262")))
        buttonList.append(QuickReplyButton(image_url=ImageConst.lookupIcon, action=MessageAction(label="lookup", text="lookup")))
        buttonList.append(QuickReplyButton(image_url=ImageConst.lookupIcon, action=MessageAction(label="lookup cooperlake", text="lookup cooperlake")))
        buttonList.append(QuickReplyButton(image_url=ImageConst.lookupIcon, action=MessageAction(label="lookup milan clock", text="lookup milan clock")))
        buttonList.append(QuickReplyButton(image_url=ImageConst.lookupIcon, action=MessageAction(label="lookup rome core 64", text="lookup rome core 64")))
        quickReply=QuickReply(items=buttonList)
        
        #Print Carousel follow with Tips and Quick Reply
        return [helpCarousel,TextSendMessage(text=AllResponse.allResponse["help"], quick_reply=quickReply)]

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
            specResponse = GetResponse.GenerateSpecAnswers(specList, selectedProduct, selectedModel)
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
            lookUpResponse = GetResponse.GenerateLookUpAnswers(specList, selectedProduct, fieldIndex, selectedValue)
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
            columnList.append(CarouselColumn(text='Page '+str(i+1), title=title, actions=actions))
        carousel_template = CarouselTemplate(columns=columnList)

        lookUpMessage = TemplateSendMessage(
            alt_text='LookUp Wizard support only on Mobile',
            template=carousel_template
        )
        return lookUpMessage

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
                line_bot_api.reply_message(token,GetResponse.GenerateHelp())
                return
        elif "spec" in words:
            line_bot_api.reply_message(token,GetResponse.GenerateSpec(words))
        elif "lookup" in words:
            line_bot_api.reply_message(token,GetResponse.GenerateLookUp(words))
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

        line_bot_api.reply_message(token,TextSendMessage(text=response))
        return   