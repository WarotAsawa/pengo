import math
import random

from linebot.models.flex_message import BoxComponent, BubbleContainer, ButtonComponent, FlexSendMessage, ImageComponent, SeparatorComponent, TextComponent
from AllResponse import AllResponse

from linebot.models import (
    TextSendMessage, QuickReplyButton, MessageAction , TemplateSendMessage, CarouselTemplate, CarouselColumn, QuickReply
)
from Converter import Converter
from Help import Help
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
    maxCapacityTB["A630"] = 277.0769
    maxCapacityTB["A650"] = 879.6093
    maxCapacityTB["A670"] = 1759.219

    #Available SSD Size
    ssdSizeList = [1.92, 3.84, 7.68, 15.36]

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
        #Get highest even num . If 4 nodes fnd cloest x4
        if driveResult >= 288 or driveResult*usableTB >= 1759.219:
            driveResult = math.floor(driveResult/4)*4
        else:
            driveResult = math.floor(driveResult/2)*2
        
        while True:
            #If result is bigger that Primera supported return 0
            if driveResult * diskSize > 1759.219*2: return 0
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
        result = ""
        all2NModel = ["A630", "A650", "A670"]
        for model in all2NModel:
            if diskCount <= maxDrive[model] and rawTB <= maxCapacityTB[model] and diskCount%2 == 0:
                result = result + " " + model + "2N"
        all4NModel = ["A650", "A670"]
        for model in all4NModel:
            if diskCount <= maxDrive[model] * 2 and rawTB <= maxCapacityTB[model] * 2 and diskCount%4 == 0:
                result = result + " " + model + "4N"
        result = result + "\n"
        return result.strip()

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
            supportedText = PrimeraSizer.GetSupportedModelFromDrives(ssdSize, diskCount)
            #If error means too big and no support model

            print(str(diskCount) + "  " + str(ssdSize) + supportedText)
            
            if (diskCount == 0): continue
            
            if supportedText == "": continue

            #Print all sizing
            config = config + 1
            rawTB = diskCount*ssdSize
            usableTB = PrimeraSizer.GetTBUsable(ssdSize, diskCount)
            diskCountText = str(diskCount) + " x " + str(ssdSize) + " TB SSD"
            rawText = str(round(rawTB,2)) + "TB / " + str(round(rawTB/Converter.TBToUnitMultipler("TiB"),2)) + "TiB"
            usableText = str(round(usableTB,2)) + "TB / " + str(round(usableTB/Converter.TBToUnitMultipler("TiB"),2)) + "TiB"
            contents.append(TextComponent(text="Config " + str(config) + " : " + str(ssdSize) + " TB SSD", weight='bold', size='sm', margin='md'))            
            contents.append(Help.AddFlexRow("SSD Config",diskCountText,3,6))
            contents.append(Help.AddFlexRow("Total Raw",rawText,3,6))
            contents.append(Help.AddFlexRow("Total Usable",usableText,3,6,weight='bold'))
            contents.append(Help.AddUsageBar(usage=(required * 100 * multiplier/usableTB)))
            contents.append(Help.AddFlexRow("Supported Model",supportedText,4,5))   
        
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
    def GenerateExampleCarousel(warning, capacity = 0):
        title = "Primera sizing example"
        exampleList = []
        textPreFix = "size primera "
        #If no capacity generate random units
        if capacity == 0:
            for i in range(0,10):
                unitRand = random.choice([" TB", " TiB"])
                capaRand = str(random.randint(1,70)*10)
                exampleList.append(capaRand+unitRand)
        else:
            #Is have capacity recommend units
            exampleList = [str(capacity)+" TB", str(capacity)+" TiB"]

        #Add FLex Content
        contents = []
        headerContents = []
        #Add Header
        headerContents.append(TextComponent(text=title, weight='bold', size='md',wrap=True))
        contents.append(TextComponent(text="Tip: size primera [required usable] [TB/TiB]", size='xs', wrap=True))
        #Add Model Button
        for i in range(0,math.floor(len(exampleList)/2)):
            buttonList = []
            buttonList.append(Help.DefaultButton(label=exampleList[i*2], text=textPreFix + exampleList[i*2]))
            buttonList.append(SeparatorComponent(margin='md'))
            buttonList.append(Help.DefaultButton(label=exampleList[i*2+1], text=textPreFix + exampleList[i*2+1]))
            box = BoxComponent(layout='horizontal',spacing='sm',contents=buttonList)
            contents.append(box)
        
        headerContents.append(BoxComponent(layout='vertical',margin='lg',spacing='sm', contents=contents))
        body = BoxComponent(layout='vertical', contents=headerContents)
        hero = ImageComponent(url=ImageConst.sizeImage,background_color=ImageConst.sizeColor,aspect_ratio='20:5',aspect_mode='fit',size='full')
        bubble = BubbleContainer(direction='ltr',body=body,hero=hero)
        bubbleMessage = FlexSendMessage(alt_text="Primera Sizing Example", contents=bubble)

        return [TextSendMessage(text=warning), bubbleMessage]

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
            if required <= 0 or required > 2711.33:  
                return PrimeraSizer.GenerateExampleCarousel("Please input capacity between 0 and 2711") 
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
                return PrimeraSizer.GenerateExampleCarousel("Please input unit as TB or TiB", capacity=required)

            #Capacity Check
            multiplier = Converter.TBToUnitMultipler(unit)
            convertedRequired = required * multiplier * 100 / utilization
            if convertedRequired <= 0 or convertedRequired > 2711.33:  
                return PrimeraSizer.GenerateExampleCarousel("Please input capacity between 0 and 2711") 
            
            #Get Sizing
            return PrimeraSizer.GeneratePrimeraSizeAnswers(unit = unit, required = required, utilization = utilization)




        