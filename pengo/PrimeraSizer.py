import math
import random

from linebot.models.flex_message import BoxComponent, BubbleContainer, FlexSendMessage, TextComponent
from AllResponse import AllResponse

from linebot.models import (
    TextSendMessage, QuickReplyButton, MessageAction , TemplateSendMessage, CarouselTemplate, CarouselColumn, QuickReply
)
from Converter import Converter
from LineConst import LineConst
from ImageConst import ImageConst

class PrimeraSizer:
    #Primera Overhead: Using A670 4N which provide max overhead
    systemOverheadTB = 2.92;

    #Alletra9000 Overhead
    #systemOverhead = 6.22;
    targetUtilization = 0.9;
    #Max Dirve supported each node Pair
    maxDrive = {}
    maxDrive["A630"] = 144
    maxDrive["A650"] = 192
    maxDrive["A670"] = 288
    #Max Capacity supported each node Pair
    maxCapacityTB = {}
    maxCapacityTB["A630"] = 250
    maxCapacityTB["A650"] = 800
    maxCapacityTB["A670"] = 1600

    #Available SSD Size
    ssdSizeList = [1.92, 3.84, 7.68, 15.36]

    @staticmethod   
    def AddFlexRow(self, title, text, titleWidth, textWidth):
        contents = []
        contents.append(TextComponent(text=title,color='#bebe66',size='sm',flex=titleWidth, wrap=True))
        contents.append(TextComponent(text=text ,color='#666666',size='sm',flex=textWidth , wrap=True))
        box = BoxComponent(layout='baseline',spacing='sm',contents=contents)
        return box
        
    @staticmethod
    def GetTBUsable(diskSize: float, diskCount: int):
        
        #Config Spare
        if diskSize < 3.84: spareRatio = 0.1
        #Set Chunklet Overhead per drive
        if diskSize > 1.92 and diskSize < 15:
            diskSize = diskSize - 0.001
        elif diskSize > 15: 
            diskSize = diskSize - 0.313

        #Defalt R6 size = 10+2 = 12
        raid6SetSize = 12
        spareTB = diskSize * 2
        rawTB = diskSize * diskCount
        spareRatio = 0.07
        #Check drive input
        if diskCount < 8 or diskCount%2 == 1:
            print("Please input diskcount as even number > 8")
            return 0

        #Adjust RAID6 size
        if diskCount < 12: raid6SetSize = diskCount

        if (diskSize * diskCount * spareRatio) > spareTB:
            spareTB = diskSize * diskCount * spareRatio;

        usableTB = (rawTB - spareTB - PrimeraSizer.systemOverheadTB) * (raid6SetSize - 2) / raid6SetSize

        return usableTB
    
    @staticmethod
    def SearchDiskCount(diskSize, usableTB):
        
        #Get Raw from Usable and multiply by 1.3
        driveResult = (usableTB/diskSize*1.3)
        #Get highest even num
        driveResult = math.floor(driveResult/2)*2
        
        while True:
            #If result is bigger that Primera supported return 0
            if driveResult * diskSize > 3200: return 0
            if driveResult > 576: return 0

            #CHeck if usable is enough
            ans = PrimeraSizer.GetTBUsable(diskSize, driveResult)
            if ans >= usableTB:
                return driveResult
            
            #Add Drive + 2 but if drive > 288 + 4 since it is 4 Node Configuration
            if driveResult >= 288:
                driveResult = driveResult + 4
            else:
                driveResult = driveResult + 2                

    @staticmethod
    def GetSupportedModelFromDrives(diskSize, diskCount):
        rawTB = diskSize * diskCount
        maxDrive = PrimeraSizer.maxDrive
        maxCapacityTB = PrimeraSizer.maxCapacityTB
        result = "Supported Model:"
        all2NModel = ["A630", "A650", "A670"]
        for model in all2NModel:
            if diskCount <= maxDrive[model] and rawTB <= maxCapacityTB[model] and diskCount%2 == 0:
                result = result + " " + model + "2N"
        all4NModel = ["A650", "A670"]
        for model in all4NModel:
            if diskCount <= maxDrive[model] * 2 and rawTB <= maxCapacityTB[model] * 2 and diskCount%4 == 0:
                result = result + " " + model + "4N"
        return result

    @staticmethod
    def GeneratePrimeraSizeAnswers(unit = "TB", required = 50.0, utilization = 100.0):
        multiplier = Converter.TBToUnitMultipler(unit)
        convertedRequired = required * multiplier * 100 / utilization
        preAnswer = AllResponse.GetRandomResponseFromKeys('preAnswer')
        answer = TextSendMessage(text='Temp')
        postAnswer = "See below similar Sizings"
        config = 0
        #Add FLex Content
        contents = []
        headerContents = []
        #Add Header
        headerContents.append(TextComponent(text='Primera Sizing Result', weight='bold', size='xl'))
        for ssdSize in PrimeraSizer.ssdSizeList:
            diskCount = PrimeraSizer.SearchDiskCount(ssdSize, convertedRequired)
            #If error means too big
            if (diskCount == 0): continue

            #Print all sizing
            config = config + 1
            rawTB = diskCount*ssdSize
            usableTB = PrimeraSizer.GetTBUsable(ssdSize, diskCount)
            diskCountText = str(diskCount) + " x " + str(ssdSize) + " TB SSD"
            rawText = "Raw : " + str(round(rawTB,2)) + "TB / " + str(round(rawTB/Converter.TBToUnitMultipler("TiB"),2)) + "TiB"
            usableText = "Usable : " + str(round(usableTB,2)) + "TB / " + str(round(usableTB/Converter.TBToUnitMultipler("TiB"),2)) + "TiB\n"
            result = result + PrimeraSizer.GetSupportedModelFromDrives(ssdSize, diskCount)
            result = result + "\n"
            contents.append(TextComponent(text="Config " + str(config), weight='bold', size='sm', margin='md'))            
            contents.append(PrimeraSizer.AddFlexRow("SSD Config",diskCountText,3,6))
            contents.append(PrimeraSizer.AddFlexRow("Total Raw",rawText,3,6))
            contents.append(PrimeraSizer.AddFlexRow("Total Usable",usableText,3,6))      
        
        #Check is OK
        if config == 0: contents = [TextComponent(text='No answers found !!', weight='bold', size='md')]
        #Add Contents
        headerContents.append(BoxComponent(layout='vertical',margin='lg',spacing='sm', contents=contents))
        body = BoxComponent(layout='vertical', contents=headerContents)
        bubble = BubbleContainer(direction='ltr',body=body)
        #Return Flex Message
        answer = FlexSendMessage(alt_text="Nimble HF Sizing Results", contents=bubble)

        #Set Quick reply for convert unit (TB,TiB) and offer 100,90% utilization sizing
        buttonList = [];
        TB100 = "TB"
        TiB100 = "TiB"
        TB90 = "TB @90%"
        TiB90 = "TiB @90%"
        strSizing = str(math.floor(required))
        newRand = random.randint(10, 1800)
        #Check if has no answers
        if  config == 0:
            preAnswer = AllResponse.GetRandomResponseFromKeys('errorWord')
            postAnswer = "No answers found !! Try these instead."
            strSizing = str(newRand)
            required = newRand

        buttonList.append(QuickReplyButton(image_url=ImageConst.sizeIcon, action=MessageAction(label=strSizing+TB100, text="size primera "+str(required)+" TB")))
        buttonList.append(QuickReplyButton(image_url=ImageConst.sizeIcon, action=MessageAction(label=strSizing+TiB100, text="size primera "+str(required)+" TiB")))
        buttonList.append(QuickReplyButton(image_url=ImageConst.sizeIcon, action=MessageAction(label=strSizing+TB90, text="size primera "+str(required)+" TB 90")))
        buttonList.append(QuickReplyButton(image_url=ImageConst.sizeIcon, action=MessageAction(label=strSizing+TiB90, text="size primera "+str(required)+" TiB 90")))

        quickReply=QuickReply(items=buttonList)

        return [TextSendMessage(text=preAnswer), answer, TextSendMessage(text=postAnswer, quick_reply=quickReply)]
        #, quick_reply=quickReply)

    @staticmethod
    def GenerateExampleCarousel(warning):
        title = "Here is some sizing example"
        textPreFix = "size primera "
        exampleList = ["10 TB", "100 TB", "150 TiB", "200.5 TiB", "500 TB", "1000 TiB"]
        columnList = []
        #Set Column and Item Limit
        maxAction = LineConst.maxCarouselColumn * LineConst.maxActionPerColumn
        #check command's len to prepare return message
        for i in range(int(math.ceil(len(exampleList)/LineConst.maxActionPerColumn))):
            if i >= LineConst.maxCarouselColumn: break
            actions = []
            for j in range(i*LineConst.maxActionPerColumn,(i*LineConst.maxActionPerColumn)+LineConst.maxActionPerColumn):
                if j >= maxAction: break
                if j >= len(exampleList):
                    actions.append(MessageAction(label=". . .",text=textPreFix))
                else:
                    actions.append(MessageAction(label=exampleList[j][0:12],text=textPreFix + exampleList[j]))
            columnList.append(CarouselColumn(thumbnail_image_url =ImageConst.sizeImage, text='Usage\nsize primera [required usable] [TB/TiB]\nPage '+str(i+1), title=title, actions=actions))
        carousel_template = CarouselTemplate(columns=columnList)
        carousel = TemplateSendMessage(
            alt_text='Sizing Wizard support only on Mobile',
            template=carousel_template
        )
        return [TextSendMessage(text=warning), carousel]

    @staticmethod
    def GeneratePrimeraSizer(words):
        if len(words) == 2:
            return PrimeraSizer.GenerateExampleCarousel("Primera Sizer Example")
        elif len(words) == 3:
            required = 0.0
            try:
                required = float(words[2])
            except ValueError:
                return PrimeraSizer.GenerateExampleCarousel("Please input capacity as Decimal") 
            if required <= 0 or required > 2721.29:  
                return PrimeraSizer.GenerateExampleCarousel("Please input capacity between 0 and 2721") 
            return PrimeraSizer.GeneratePrimeraSizeAnswers(unit = "TB", required = required)
        elif len(words) > 3:
            required = 0.0
            #add utilization
            utilization = 100.0
            if len(words) > 4:
                try: utilization = float(words[4])
                except ValueError: utilization = 100.0
            if utilization <= 0: utilization = 1.0
            if utilization > 100: utilization = 100.0

            try:
                required = float(words[2])
            except ValueError:
                return PrimeraSizer.GenerateExampleCarousel("Please input capacity as Decimal") 
            
            #Check if unit is tb or tib
            unit = words[3].lower()
            unitCheck = ["tb","tib"]
            #unitCheck = ["tb","tib", "gb", "gib", "pb", "pib"]
            if unit not in unitCheck:
                return PrimeraSizer.GenerateExampleCarousel("Please input unit as TB or TiB") 
            #Capacity Check
            multiplier = Converter.TBToUnitMultipler(unit)
            convertedRequired = required * multiplier * 100 / utilization
            if convertedRequired <= 0 or convertedRequired > 2721.29:  
                return PrimeraSizer.GenerateExampleCarousel("Please input capacity between 0 and 2721") 
            #Get Sizing
            return PrimeraSizer.GeneratePrimeraSizeAnswers(unit = unit, required = required, utilization = utilization)




        