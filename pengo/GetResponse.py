import random;
import csv;
import os;
import math;

from linebot import (
    LineBotApi
)
from linebot.models import (
    TextSendMessage, QuickReplyButton, MessageAction , TemplateSendMessage, CarouselTemplate, CarouselColumn, QuickReply
)
class GetResponse:
    #CSV Path
    csvPath = './data/'
    #LINE Limitation
    maxQuickReply = 13
    maxCarouselColumn = 10
    maxActionPerColumn = 3
    #Icons Image URL
    specIcon = 'https://github.com/WarotAsawa/pengo/raw/main/public/img/spec_icon.png'
    lookupIcon = 'https://github.com/WarotAsawa/pengo/raw/main/public/img/lookup_icon.png'
    specImage = 'https://github.com/WarotAsawa/pengo/raw/main/public/img/spec_image.png'
    lookupImage = 'https://github.com/WarotAsawa/pengo/raw/main/public/img/lookup_image.png'
    helpImgURL = 'https://warotasawa.files.wordpress.com/2020/07/how2.png'
    #Response String
    allResponse = {};
    allResponse["help"] = "You can see what I can do listed on the Carousel above. Tap on each item or you quick reply below for example"
    allResponse["helpspec"] = "Type \"spec\" for wizard or use or use \nspec [productname] [model] \n ex: \n - spec 3par 8200\n - spec nimble af20"
    allResponse["helplookup"] =  "Type \"lookup\" for wizard or use or use \nlookup [productname] [attribute] [value] \n ex: \n - lookup intel core 20\n - lookup amd clock 3.3"
    allResponse["helptips"] = ["Ask me for 'help' to see what I can do for you","Want to learn how to talk to me? Ask me for 'help'.","Ask for 'help' to see how smart I am."]
    allResponse["hello"] = ["Hello there , ","Hello, ", "What's up, ", "Good day, ", "Hi, ","May I help you, ","Greetings, ","How can I help you, "]
    allResponse["thank"] = ["You are always welcome.","With pleasure.","I am glad to be your service.","My pleasure.","You can ask me for help anytime."]
    allResponse["bye"] = ["I'll be back, ", "Bye bye, ", "So longgg, ", "Hasta la vista, ", "Sayonara, ", "Life is too short to say goodbye, "]
    allResponse["whatyourname"] = ["Don'you see my name above?","My name is Uvuvwevwevwe Onyetenyevwe Ugwemubwem Ossas","I am the one called YOU KNOW WHO.","I am the Dark Lord.","Kimino na wa!"]
    allResponse["whatyoudo"] = ["I am chatting with you,seriously.","Texting texting texting texting texting texting texting","Chit chat! I am Chit-chatting.","I am talking with an idiot.","I have no idea what I am doing right now."]
    allResponse["whatareyou"] = ["I am your worst nightmare.","I am a human being","I am Batman!","I am your shadow.","I am you."]
    allResponse["what"] = ["What !??","Wattttt?","What is what ?","What is a pronoun to ask for information specifying something.","Duhhhh","What are you talking about?"]
    allResponse["where"] = ["Where is a matter of place not a matter of time.","This universe is really big don't you think?","That's use to ask in or to what place or position","Where is what?","I don't know. Duhhh!"]
    allResponse["when"] = ["When is a matter of time not a matter of place.","This universe heat death is very long.","At any moment now.","When is what?","How do I know?","I don' know. Duhhh!"]
    allResponse["why"] = ["Because it is my demand.","Because it is an order from god. And I am your god now.","Do not seek for a reason. Everything has its own purpose.","Because nothing is true. Everything is permitted.","Why should I know?"]
    allResponse["whoareyou"] = ["I am your worst nightmare.","I am a creature called Homosapiean","I am Batman!","I am your shadow.","I am you."]
    allResponse["who"] = ["Who ??","Each and Everyone.","No body.","Just you and me my friend.","Why should I know?","I don't know. Duhhh!"]
    allResponse["howareyou"] = ["No. Not good. NOT GOOD! ","I'm fine thank you and you? ","I felt terrible. ","Never been this good. ","I feel selfless. "]
    allResponse["how"] = ["I do not know how.","How sould I know?","No idea. Duhhh"]
    allResponse["canyou"] = ["No. I can't do somthing like that.","No. I don't have an ability to do that","I dont have time for that !"]
    allResponse["youwantto"] = ["I don't want that one bit.","Why should I do that?","Seriously!?","Never !!"]
    allResponse["youhaveto"] = ["I don't take orders from you.","What are you now,aster?","Stop tell me what to do.","Never !!","Give me one reason why should I trust you.","Roger roger.","Fine.","OK then."]
    allResponse["cani"] = ["For god's sake,T","Please.","Seriously,t","Do it now.","Don't do it.","Stop. STOPPPPPPP","Go on","Just don't.","Just do it","This need to be stop.","Who cares.","It's now or never."]
    allResponse["really"] = ["Indeed,s.","Oh sure.","Yes!"]
    allResponse["fuck"] = ["No F word ,please.","You should said Firetruck instead.","Please be polite!"]
    allResponse["joke"] = ["I would tell you a chemistry joke but I know I wouldnt get a reaction.","Why dont some couples go to the gym? Because some relationships dont work out.","I wondered why the baseball was getting bigger. Then it hit me.","Have you ever tried to eat a clock? It is very time consuming.","The experienced carpenter really nailed it,but the new guy screwed everything up.","Did you hear about the guy whose whole left side was cut off? He is all right now.","Yesterday I accidentally swallowed some food coloring. The doctor says I am OK,but I feel like I have dyed a little inside.","I wasnt originally going to get a brain transplant,but then I changed my mind.","A guy was admitted to hospital with 8 plastic horses in his stomach. His condition is now stable.."," If a wild pig kills you,does it mean you’ve been boared to death?","You cry,I cry,…you laugh,I laugh…you jump off a cliff I laugh even harder!!","Never steal. The government hates competition.","Doesn’t expecting the unexpected make the unexpected expected?","Practice makes perfect but then nobody is perfect so what’s the point of practicing?","Everybody wishes they could go to heaven but no one wants to die.","Why are they called apartments if they are all stuck together?","DON’T HIT KIDS!!! No,seriously,they have guns now.","Save paper,don’t do home work.","Do not drink and drive or you might spill the drink.","Life is Short – Talk Fast!","Why do stores that are open 24/7 have locks on their doors?","When nothing goes right,Go left.","Save water ,do not shower.","A Lion would never cheat on his wife but a Tiger Wood.","Why do they put pizza in a square box?"]
    allResponse["errorWord"] =["Please give me a valid input.","No, I am too dumb to do that.","Please try again.","I do not get that.","You mad? ","You have to ask me again."]
    allResponse["preAnswer"] = ["Ok Ok Ok.","This looks hardish, but I am smart enought to do this.","Piece of cake!.","Oh too easy.","You will thank me for this later.","Here you go.","There you go.","Here is you answers."]
    #Create 2D Array from CSV File
    @staticmethod
    def GetArrayFromCSV(fileName):
        with open(fileName, newline='') as f:
            reader = csv.reader(f)
            data = list(reader)
            return data

    #Get Random string from allResponse via key
    @staticmethod
    def GetRandomResponseFromKeys(key):
        i = random.randint(0, len(GetResponse.allResponse[key])-1 )
        return GetResponse.allResponse[key][i]

    #Generate Spec Reply String
    @staticmethod
    def GenerateSpecAnswers(specList, selectedProduct, selectedModel):
        fieldList = specList[0];
        unitList = specList[1];
        index = 0;
        #Prepare string response
        response = GetResponse.GetRandomResponseFromKeys('preAnswer') + "\n"
        response = response + "Here is the Spec of : " + selectedProduct + " " + selectedModel

        for i in range(2,len(specList)):
            model = specList[i][0]
            if selectedModel == model:
                index = i
                break
        if i==0: return TextSendMessage(text=GetResponse.GetRandomResponseFromKeys('errorWord'))
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
        response = GetResponse.GetRandomResponseFromKeys('preAnswer') + "\n"
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
            if i >= GetResponse.maxQuickReply: break
            specText = "spec " + selectedProduct + " " + allMatchModel[i]
            buttonList.append(QuickReplyButton(image_url=GetResponse.specIcon, action=MessageAction(label=allMatchModel[i], text=specText)))

        if count == 0:
            response = GetResponse.GetRandomResponseFromKeys('errorWord') + "\n"
            response = response + "Cannot find any model of : " + selectedProduct + ", which " + fieldList[fieldIndex] + " is " + selectedValue + " " + unitList[fieldIndex];
            #Add quickreply for lookup for other value
            buttonList = []
            for i in range(len(uniqueValue)):
                if i >= GetResponse.maxQuickReply: break
                lookupText = "lookup " + selectedProduct + " " + fieldList[fieldIndex] + " " + uniqueValue[i]
                buttonList.append(QuickReplyButton(image_url=GetResponse.lookupIcon, action=MessageAction(label=uniqueValue[i], text=lookupText)))
        
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
        columnList.append(CarouselColumn(thumbnail_image_url =GetResponse.specImage, title=specTitle, text=specText, actions=specAction))
        columnList.append(CarouselColumn(thumbnail_image_url =GetResponse.lookupImage, title=lookUpTitle, text=lookUpText, actions=lookUpAction))
        carousel_template = CarouselTemplate(columns=columnList)
        helpCarousel = TemplateSendMessage(
            alt_text='Help Wizard support only on Mobile',
            template=carousel_template
        )
        #Create QuickReply ButtonList
        
        buttonList = [];
        buttonList.append(QuickReplyButton(image_url=GetResponse.specIcon, action=MessageAction(label="spec", text="spec")))
        buttonList.append(QuickReplyButton(image_url=GetResponse.specIcon, action=MessageAction(label="spec nimble", text="spec nimble")))
        buttonList.append(QuickReplyButton(image_url=GetResponse.specIcon, action=MessageAction(label="spec primera A630", text="spec primera A630")))
        buttonList.append(QuickReplyButton(image_url=GetResponse.specIcon, action=MessageAction(label="spec rome 7262 ", text="spec rome 7262")))
        buttonList.append(QuickReplyButton(image_url=GetResponse.lookupIcon, action=MessageAction(label="lookup", text="lookup")))
        buttonList.append(QuickReplyButton(image_url=GetResponse.lookupIcon, action=MessageAction(label="lookup cooperlake", text="lookup cooperlake")))
        buttonList.append(QuickReplyButton(image_url=GetResponse.lookupIcon, action=MessageAction(label="lookup milan clock", text="lookup milan clock")))
        buttonList.append(QuickReplyButton(image_url=GetResponse.lookupIcon, action=MessageAction(label="lookup rome core 64", text="lookup rome core 64")))
        quickReply=QuickReply(items=buttonList)
        
        #Print Carousel follow with Tips and Quick Reply
        return [helpCarousel,TextSendMessage(text=GetResponse.allResponse["help"], quick_reply=quickReply)]

    #Generate spec output
    @staticmethod
    def GenerateSpec(words):
        fileList = os.listdir(GetResponse.csvPath)
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
            errorMessage = GetResponse.GetRandomResponseFromKeys("errorWord") + "\nPlease type \"spec\" or Select one of these product:\n"
            for product in productList:
                errorMessage = errorMessage + "\n - " + product;
                if words[1] == product.strip().lower():
                    selectedProduct = product
            #If No matched product, return Error Message Else got Model List
            if selectedProduct == "":
                return [TextSendMessage(text=errorMessage)]

            #Get Product's Model List
            specList = GetResponse.GetArrayFromCSV(GetResponse.csvPath+selectedProduct+".csv")
            for i in range(2,len(specList)):
                model = str(specList[i][0])
                modelList.append(model)
                
        #Check if Model name is valide and output error
        if (len(words) > 2):
            errorMessage = GetResponse.GetRandomResponseFromKeys("errorWord") + "\nPlease type \"spec " + selectedProduct + "\" or Select one of these model:\n"
            for model in modelList:
                errorMessage = errorMessage + model + " "
                if words[2] == model.strip().lower():
                    selectedModel = model
            #If No matched model, return Error Message Else got Model List
            if selectedModel == "":
                return [TextSendMessage(text=errorMessage)]
        
        #Set Column and Item Limit
        maxAction = GetResponse.maxCarouselColumn * GetResponse.maxActionPerColumn
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
        for i in range(int(math.ceil(len(loopList)/GetResponse.maxActionPerColumn))):
            if i >= GetResponse.maxCarouselColumn: break
            actions = []
            for j in range(i*GetResponse.maxActionPerColumn,(i*GetResponse.maxActionPerColumn)+GetResponse.maxActionPerColumn):
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
        fileList = os.listdir(GetResponse.csvPath)
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
            errorMessage = GetResponse.GetRandomResponseFromKeys("errorWord") + "\nPlease type \"lookUp\" or Select one of these product:\n"
            for product in productList:
                errorMessage = errorMessage + "\n - " + product;
                if words[1] == product.strip().lower():
                    selectedProduct = product
            #If No matched product, return Error Message Else got Model List
            if selectedProduct == "":
                return [TextSendMessage(text=errorMessage)]

            #Get Product's Field List
            specList = GetResponse.GetArrayFromCSV(GetResponse.csvPath+selectedProduct+".csv")
            for i in range(1,len(specList[0])):
                field = str(specList[0][i])
                fieldList.append(field)
                
        #Check if Field name is valide and output error
        if (len(words) > 2):
            errorMessage = GetResponse.GetRandomResponseFromKeys("errorWord") + "\nPlease type \"lookUp " + selectedProduct + "\" or Select one of these field:\n"
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
                value = str(specList[i][fieldIndex]).strip()
                if value not in valueList:
                    valueList.append(value)
        
        #Check if input already field's value
        if (len(words) > 3):
            for i in range(3,len(words)):
                selectedValue = selectedValue + words[i] + " "
            selectedValue = selectedValue.strip().lower()
        #Set Column and Item Limit
        maxAction = GetResponse.maxCarouselColumn * GetResponse.maxActionPerColumn
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
        for i in range(int(math.ceil(len(loopList)/GetResponse.maxActionPerColumn))):
            if i >= GetResponse.maxCarouselColumn: break
            actions = []
            for j in range(i*GetResponse.maxActionPerColumn,(i*GetResponse.maxActionPerColumn)+GetResponse.maxActionPerColumn):
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
                response = GetResponse.allResponse["helpspec"]
            elif "lookup" in words:
                response = GetResponse.allResponse["helplookup"]
            else:
                line_bot_api.reply_message(token,GetResponse.GenerateHelp())
                return
        elif "spec" in words:
            line_bot_api.reply_message(token,GetResponse.GenerateSpec(words))
        elif "lookup" in words:
            line_bot_api.reply_message(token,GetResponse.GenerateLookUp(words))
        elif "hello" in words or "hi" in words or "greet" in words:
            response = GetResponse.GetRandomResponseFromKeys('hello')
        elif "thank" in words:
            response = GetResponse.GetRandomResponseFromKeys('thank')
        elif "bye" in words:
            response = GetResponse.GetRandomResponseFromKeys('bye')
        elif "why" in words:
            response = GetResponse.GetRandomResponseFromKeys('why')
        elif "when" in words:
            response = GetResponse.GetRandomResponseFromKeys('when')
        elif "where" in words:
            response = GetResponse.GetRandomResponseFromKeys('where')
        elif "how" in words:
            if "are" in words and "you" in words:
                response = GetResponse.allResponse["howareyou"]
            else:
                response = GetResponse.GetRandomResponseFromKeys('how')
        else:
            response = GetResponse.GetRandomResponseFromKeys('joke') + "\n\n" + GetResponse.GetRandomResponseFromKeys('helptips')

        line_bot_api.reply_message(token,TextSendMessage(text=response))
        return   