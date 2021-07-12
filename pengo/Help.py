import math

from linebot.models import (
    TextSendMessage, QuickReplyButton, MessageAction , TemplateSendMessage, CarouselTemplate, CarouselColumn, QuickReply
)
from linebot.models.flex_message import BoxComponent, TextComponent

from AllResponse import AllResponse
from ImageConst import ImageConst
from LineConst import LineConst

class Help:
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
        #Sizer Help Menu
        sizeTitle = 'size :Quick Sizing for each product'
        sizeText = 'Tip: size [product]\nOr tab below to start'
        sizeAction = []
        sizeAction.append(MessageAction(label="size",text='size'))
        sizeAction.append(MessageAction(label="size primera",text='size primera'))
        sizeAction.append(MessageAction(label="size nimble",text='size nimble'))
        # Create Column List for Carosel
        columnList = []
        columnList.append(CarouselColumn(thumbnail_image_url =ImageConst.specImage, title=specTitle, text=specText, actions=specAction))
        columnList.append(CarouselColumn(thumbnail_image_url =ImageConst.lookupImage, title=lookUpTitle, text=lookUpText, actions=lookUpAction))
        columnList.append(CarouselColumn(thumbnail_image_url =ImageConst.sizeImage, title=sizeTitle, text=sizeText, actions=sizeAction))

        carousel_template = CarouselTemplate(columns=columnList)
        helpCarousel = TemplateSendMessage(
            alt_text='Help Wizard support only on Mobile',
            template=carousel_template
        )
        
        #Print Carousel follow with Tips and Quick Reply
        return [TextSendMessage(text=AllResponse.allResponse["help"]), helpCarousel]

    @staticmethod
    def GeneralHelp():
        #Create QuickReply ButtonList
        buttonList = [];
        buttonList.append(QuickReplyButton(image_url=ImageConst.helpIcon, action=MessageAction(label="help", text="help")))
        buttonList.append(QuickReplyButton(image_url=ImageConst.specIcon, action=MessageAction(label="spec", text="spec")))
        buttonList.append(QuickReplyButton(image_url=ImageConst.lookupIcon, action=MessageAction(label="lookup", text="lookup")))
        buttonList.append(QuickReplyButton(image_url=ImageConst.sizeIcon, action=MessageAction(label="size", text="size")))
        quickReply=QuickReply(items=buttonList)
        return quickReply

    @staticmethod
    def GenerateCarousel(type="spec product", list=[], selectedProduct="",selectedField=""):
        textPreFix = ""
        imageUrl = ImageConst.specImage
        loopList = list

        #Set initial menu text
        if type == "spec product": 
            imageUrl = ImageConst.specImage
            textPreFix = "spec "
            title = "Choose Your Product for Spec"
        elif type == "spec model": 
            imageUrl = ImageConst.specImage
            textPreFix = "spec " + selectedProduct + " "
            title = "Choose Your Model for Spec"
        elif type == "lookup product": 
            imageUrl = ImageConst.lookupImage
            textPreFix = "lookup "
            title = "Choose Your Field for Lookup"
        elif type == "lookup field": 
            imageUrl = ImageConst.lookupImage
            textPreFix = "lookup " + selectedProduct + " "
            title = "Choose Your Model for Lookup"
        elif type == "lookup value": 
            imageUrl = ImageConst.lookupImage
            textPreFix = "lookup " + selectedProduct + " " + selectedField + " "
            title = "Choose Your Value for Lookup"

        
        #Set Column and Item Limit
        maxAction = LineConst.maxCarouselColumn * LineConst.maxActionPerColumn
        #Create Carosel Colume base on product or Model or Field
        columnList = [];
        for i in range(int(math.ceil(len(loopList)/LineConst.maxActionPerColumn))):
            if i >= LineConst.maxCarouselColumn: break
            actions = []
            for j in range(i*LineConst.maxActionPerColumn,(i*LineConst.maxActionPerColumn)+LineConst.maxActionPerColumn):
                if j >= maxAction: break
                if j >= len(loopList):
                    actions.append(MessageAction(label=". . .",text=textPreFix))
                else:
                    actions.append(MessageAction(label=loopList[j][0:12],text=textPreFix + loopList[j]))
            columnList.append(CarouselColumn(thumbnail_image_url =imageUrl, text='Page '+str(i+1), title=title, actions=actions))
        carousel_template = CarouselTemplate(columns=columnList)

        message = TemplateSendMessage(
            alt_text='LookUp Wizard support only on Mobile',
            template=carousel_template
        )
        return message

    
    @staticmethod   
    def AddFlexRow(title, text, titleWidth, textWidth, color = '#00b088', weight = 'regular'):
        contents = []
        contents.append(TextComponent(text=title,color=color,size='sm',flex=titleWidth, wrap='regular'))
        contents.append(TextComponent(text=text ,color='#666666',size='sm',flex=textWidth , wrap=True, weight=isBold))
        box = BoxComponent(layout='baseline',spacing='sm',contents=contents)
        return box