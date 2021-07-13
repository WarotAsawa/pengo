import math

from linebot.models.flex_message import BoxComponent, BubbleContainer, ButtonComponent, FlexSendMessage, ImageComponent, TextComponent, CarouselContainer

from linebot.models import (
    TextSendMessage, QuickReplyButton, MessageAction , TemplateSendMessage, CarouselTemplate, CarouselColumn, QuickReply
)
from linebot.models.flex_message import BoxComponent, TextComponent

from AllResponse import AllResponse
from ImageConst import ImageConst
from LineConst import LineConst

class Help:
    #Variable
    specToolTip =       "Find specification for each product model\nTip: spec [product] [model]"
    lookupToolTip =     "Lookup match model for selected field value\nTip: lookup [product] [field] [value]"
    sizeToolTip =       "Tip: size [product] [model] [size] [TB/TiB]"
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
        tooltip = ""
        imageUrl = ImageConst.specImage
        loopList = list
        
        bgColor = '#'
        #Set initial menu text
        if type == "spec product": 
            imageUrl = ImageConst.specImage
            textPreFix = "spec "
            title = "Choose Your Product"
            tooltip = Help.specToolTip
            bgColor = ImageConst.specColor
        elif type == "spec model": 
            imageUrl = ImageConst.specImage
            textPreFix = "spec " + selectedProduct + " "
            title = "Choose Your Model"
            tooltip = Help.specToolTip
            bgColor = ImageConst.specColor
        elif type == "lookup product": 
            imageUrl = ImageConst.lookupImage
            textPreFix = "lookup "
            title = "Choose Your Field for Lookup"
            tooltip = Help.lookupToolTip
            bgColor = ImageConst.lookupColor
        elif type == "lookup field": 
            imageUrl = ImageConst.lookupImage
            textPreFix = "lookup " + selectedProduct + " "
            title = "Choose Your Model"
            tooltip = Help.lookupToolTip
            bgColor = ImageConst.lookupColor
        elif type == "lookup value": 
            imageUrl = ImageConst.lookupImage
            textPreFix = "lookup " + selectedProduct + " " + selectedField + " "
            title = "Choose Your Value"
            tooltip = Help.lookupToolTip
            bgColor = ImageConst.lookupColor
        elif type == 'size product':
            imageUrl = ImageConst.sizeImage
            textPreFix = "size "
            title = "Choose your Product"
            tooltip = Help.sizeToolTip
            bgColor = ImageConst.specColor

        #Set Column and Item Limit
        maxActionPerColumn = 5
        if len(list) > 60: maxActionPerColumn = math.ceil(len(list)/12)

        #Create Carosel Colume base on product or Model or Field
        bubbleList = [];
        for i in range(int(math.ceil(len(loopList)/maxActionPerColumn))):
            if i >= LineConst.maxCarouselColumn: break
            #Add FLex Content
            contents = []
            headerContents = []
            #Add Header
            headerContents.append(TextComponent(text=title, weight='bold', size=''))
            contents.append(TextComponent(text=tooltip, weight='bold', size='sm', margin='md'))
            for j in range(i*maxActionPerColumn,(i*maxActionPerColumn)+maxActionPerColumn):
                if j >= len(loopList): break
                else:
                    contents.append(ButtonComponent(color='#eeeeee',style='secondary',height='sm',action=MessageAction(label=loopList[j], text=textPreFix + loopList[j])))
             #Add Bubble's Content
            headerContents.append(BoxComponent(layout='vertical',margin='lg',spacing='sm', contents=contents))
            body = BoxComponent(layout='vertical', contents=headerContents)
            hero = ImageComponent(url=imageUrl,background_color=bgColor,aspect_ratio='20:5',aspect_mode='fit',size='full')
            bubble = BubbleContainer(direction='ltr',body=body, hero=hero)
            bubbleList.append(bubble)

        carousel_template = CarouselContainer(contents=bubbleList)

        message = FlexSendMessage(alt_text=type+" carousel", contents=carousel_template)
        return message

    
    @staticmethod   
    def AddFlexRow(title, text, titleWidth, textWidth, color = '#00b088', weight = 'regular'):
        contents = []
        contents.append(TextComponent(text=title,color=color,size='sm',flex=titleWidth, wrap=True))
        contents.append(TextComponent(text=text ,color='#666666',size='sm',flex=textWidth , wrap=True, weight=weight))
        box = BoxComponent(layout='baseline',spacing='sm',contents=contents)
        return box