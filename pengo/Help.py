from linebot.models import (
    TextSendMessage, QuickReplyButton, MessageAction , TemplateSendMessage, CarouselTemplate, CarouselColumn, QuickReply
)

from AllResponse import AllResponse
from ImageConst import ImageConst

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
        #Create QuickReply ButtonList
        
        buttonList = [];
        buttonList.append(QuickReplyButton(image_url=ImageConst.specIcon, action=MessageAction(label="spec", text="spec")))
        buttonList.append(QuickReplyButton(image_url=ImageConst.specIcon, action=MessageAction(label="spec nimble", text="spec nimble")))
        buttonList.append(QuickReplyButton(image_url=ImageConst.specIcon, action=MessageAction(label="spec rome 7262 ", text="spec rome 7262")))
        buttonList.append(QuickReplyButton(image_url=ImageConst.lookupIcon, action=MessageAction(label="lookup", text="lookup")))
        buttonList.append(QuickReplyButton(image_url=ImageConst.lookupIcon, action=MessageAction(label="lookup cooperlake", text="lookup cooperlake")))
        buttonList.append(QuickReplyButton(image_url=ImageConst.lookupIcon, action=MessageAction(label="lookup rome core 64", text="lookup rome core 64")))
        buttonList.append(QuickReplyButton(image_url=ImageConst.sizeIcon, action=MessageAction(label="size", text="size")))
        buttonList.append(QuickReplyButton(image_url=ImageConst.sizeIcon, action=MessageAction(label="size primera", text="size primera")))
        buttonList.append(QuickReplyButton(image_url=ImageConst.sizeIcon, action=MessageAction(label="size nimble", text="size nimble")))
        quickReply=QuickReply(items=buttonList)
        
        #Print Carousel follow with Tips and Quick Reply
        return [helpCarousel,TextSendMessage(text=AllResponse.allResponse["help"], quick_reply=quickReply)]

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
