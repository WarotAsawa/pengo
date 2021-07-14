import math
from os import stat
from typing import Text

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

    #Default Flex Button
    @staticmethod
    def DefaultButton(label, text):
        return ButtonComponent(color='#eeeeee',style='secondary',height='sm',action=MessageAction(label=label,text=text))
    #Generate help output
    @staticmethod
    def GenerateHelp():
        bubbleList = []
        #Hero Help Menu
        heroTitle = "I'm PenGo !!!"
        heroText = "I am PenGo and I am a very convenient Bot for my creator. You can say hello or talk with me.\n\nBy the way, you can scroll left to see what I can do !!"
        #Add Hero
        contents = []
        headerContents = []
        #Add Header
        headerContents.append(TextComponent(text=heroTitle, weight='bold', size='md'))
        contents.append(TextComponent(text=heroTitle, size='xs', wrap=True))
        contents.append(TextComponent(text=heroText, size='sm', wrap=True))
        contents.append(ButtonComponent(color='#ff3f3f',style='primary',height='sm',action=MessageAction(label="DISCLAIMER",text='disclaimer')))
        #Add Bubble's Content
        headerContents.append(BoxComponent(layout='vertical',margin='lg',spacing='sm', contents=contents))
        body = BoxComponent(layout='vertical', contents=headerContents)
        hero = ImageComponent(url=ImageConst.heroImage,aspect_ratio='1.51:1',aspect_mode='fit',size='full')
        bubbleList.append(BubbleContainer(direction='ltr',body=body,hero=hero))

        #Spec Help Menu
        specTitle = 'spec :Show detail of product\'s model'
        specText = 'Tip: spec [product] [model]\nOr tab below to start'
        #Add FLex Content
        contents = []
        headerContents = []
        #Add Header
        headerContents.append(TextComponent(text=specTitle, weight='bold', size='md'))
        contents.append(TextComponent(text=specText, size='xs', wrap=True))
        contents.append(Help.DefaultButton(label="spec",text='spec'))
        contents.append(Help.DefaultButton(label="spec nimble",text='spec nimble'))
        contents.append(Help.DefaultButton(label="spec rome 7262",text='spec rome 7262'))
        contents.append(Help.DefaultButton(label="spec simplivity 380-XL",text='spec simplivity 380-XL'))
        #Add Bubble's Content
        headerContents.append(BoxComponent(layout='vertical',margin='lg',spacing='sm', contents=contents))
        body = BoxComponent(layout='vertical', contents=headerContents)
        hero = ImageComponent(url=ImageConst.specImage,aspect_ratio='1.51:1',aspect_mode='fit',size='full')
        bubbleList.append(BubbleContainer(direction='ltr',body=body,hero=hero))
        
        #Lookup Help Menu
        lookUpTitle = 'lookup :Search product\'s model by spec'
        lookUpText = 'Tip: lookup [product] [spec] [value]\nOr tab below to start'
        #Add FLex Content
        contents = []
        headerContents = []
        #Add Header
        headerContents.append(TextComponent(text=lookUpTitle, weight='bold', size='md'))
        contents.append(TextComponent(text=lookUpText, size='xs', wrap=True))
        contents.append(Help.DefaultButton(label="lookup",text='lookup'))
        contents.append(Help.DefaultButton(label="lookup milan",text='lookup milan'))
        contents.append(Help.DefaultButton(label="lookup rome core 64",text='lookup rome core 64'))
        contents.append(Help.DefaultButton(label="lookup cascadelake clock 2.1",text='lookup cascadelake clock 2.1'))
        #Add Bubble's Content
        headerContents.append(BoxComponent(layout='vertical',margin='lg',spacing='sm', contents=contents))
        body = BoxComponent(layout='vertical', contents=headerContents)
        hero = ImageComponent(url=ImageConst.lookupImage,aspect_ratio='1.51:1',aspect_mode='fit',size='full')
        bubbleList.append(BubbleContainer(direction='ltr',body=body,hero=hero))
        
        #Sizer Help Menu
        sizeTitle = 'size :Quick Sizing for each product'
        sizeText = 'Tip: size [product]\nOr tab below to start'
        #Add FLex Content
        contents = []
        headerContents = []
        #Add Header
        headerContents.append(TextComponent(text=sizeTitle, weight='bold', size='md'))
        contents.append(TextComponent(text=sizeText, size='xs', wrap=True))
        contents.append(Help.DefaultButton(label="size",text='size'))
        contents.append(Help.DefaultButton(label="size primera",text='size primera'))
        contents.append(Help.DefaultButton(label="size nimble",text='size nimble'))
        contents.append(Help.DefaultButton(label="size simplivity",text='size simplivity'))
        #Add Bubble's Content
        headerContents.append(BoxComponent(layout='vertical',margin='lg',spacing='sm', contents=contents))
        body = BoxComponent(layout='vertical', contents=headerContents)
        hero = ImageComponent(url=ImageConst.sizeImage,aspect_ratio='1.51:1',aspect_mode='fit',size='full')
        bubbleList.append(BubbleContainer(direction='ltr',body=body,hero=hero))
        
        carousel_template = CarouselContainer(contents=bubbleList)

        helpCarousel = FlexSendMessage(alt_text="Help Menu", contents=carousel_template)
        
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
            bgColor = ImageConst.sizeColor

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
            headerContents.append(TextComponent(text=title, weight='bold', size='md'))
            contents.append(TextComponent(text=tooltip, size='xs', wrap=True))
            for j in range(i*maxActionPerColumn,(i*maxActionPerColumn)+maxActionPerColumn):
                if j >= len(loopList): break
                else:
                    contents.append(Help.DefaultButton(label=loopList[j][0:40], text=textPreFix + loopList[j]))
             #Add Bubble's Content
            headerContents.append(BoxComponent(layout='vertical',margin='lg',spacing='sm', contents=contents))
            body = BoxComponent(layout='vertical', contents=headerContents)
            hero = ImageComponent(url=imageUrl,background_color=bgColor,aspect_ratio='20:5',aspect_mode='fit',size='full')
            bubble = BubbleContainer(direction='ltr',body=body,hero=hero)
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

    @staticmethod   
    def AddUsageBar(usage = 90.0, color = '#00b088', title='Total Usage', warning = 90.0):
        usageText = str(round(usage,1)) + "%"
        usageColor = '#00b088'
        if usage > (100.0+warning)/2: 
            usageColor = ImageConst.specColor
        elif usage > warning:
            usageColor = ImageConst.sizeColor

        usageBox = BoxComponent(layout='vertical',spacing='sm',height='6px', background_color=usageColor, corner_radius='3px', width=usageText)
        totalBox = BoxComponent(layout='vertical',spacing='sm',height='6px', background_color='#dddddd', corner_radius='3px', flex=4, contents=[usageBox])
        contents = []
        contents.append(TextComponent(text=title,color=color,size='sm',flex=3, wrap=True))
        contents.append(totalBox)
        contents.append(TextComponent(text=usageText ,color='#666666',size='sm',flex=2, align='end', wrap=True))
        box = BoxComponent(layout='horizontal',spacing='sm', align_items='center',contents=contents)
        return box

    @staticmethod
    def GenerateDisclaimer():
        #Add FLex Content
        contents = []
        headerContents = []
        #Add Header
        tooltip1 = "Whlist PenGo's creator endeavour to keep information up to date and corrent. Every information was researched from public information hence the information is not own by the creator. The creator makes no representation or warranties of completeness, accuracy, availability of the infomation."
        tooltip2 = "Any reliance you place on PenGo's information is therefore strictly at your own risk."
        headerContents.append(TextComponent(text="Disclaimer", weight='bold', size='md'))
        contents.append(TextComponent(text=tooltip1, size='xs', wrap=True))
        contents.append(TextComponent(text=tooltip2, size='xs', wrap=True))

        #Add Bubble's Content
        headerContents.append(BoxComponent(layout='vertical',margin='lg',spacing='sm', contents=contents))
        body = BoxComponent(layout='vertical', contents=headerContents)
        hero = ImageComponent(url=ImageConst.disclaimerImage,aspect_ratio='1.51:1',aspect_mode='fit',size='full')
        bubble = BubbleContainer(direction='ltr',body=body,hero=hero)

        message = FlexSendMessage(alt_text="Disclaimer", contents=bubble)
        return message