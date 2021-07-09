import math

from linebot.models import (
    TextSendMessage, QuickReplyButton, MessageAction , TemplateSendMessage, CarouselTemplate, CarouselColumn, QuickReply
)
from Converter import Converter
from LineConst import LineConst

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
    def GetTBUsable(diskSize, diskCount):
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

        #Config Spare
        if diskSize < 3.84: spareRatio = 0.1
        #Set Chunklet Overhead per drive
        if diskSize == 3.84: diskSize = 3.839
        elif diskSize == 7.68: diskSize = 7.679
        elif diskSize == 15.36: diskSize = 15.047

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
    def GeneratePrimeraSizeAnswers(unit = "TB", required = 50.0):
        multiplier = Converter.TBToUnitMultipler(unit)
        required = required * multiplier
        result = ""
        config = 0
        for ssdSize in PrimeraSizer.ssdSizeList:
            diskCount = PrimeraSizer.SearchDiskCount(ssdSize, required)
            #If error means too big
            if (diskCount == 0): continue

            #Print all sizing
            config = config + 1
            rawTB = diskCount*ssdSize
            usableTB = PrimeraSizer.GetTBUsable(ssdSize, diskCount)
            result = result + "\n"
            result = result + "Config " + str(config) + ":\n"
            result = result + str(diskCount) + " x " + str(ssdSize) + "TB SSD\n"
            result = result + "Raw : " + str(round(rawTB,2)) + " TB / " + str(round(rawTB/Converter.TBToUnitMultipler("TiB"),2)) + " TiB\n"
            result = result + "Usable : " + str(round(usableTB,2)) + " TB / " + str(round(usableTB/Converter.TBToUnitMultipler("TiB"),2)) + " TiB\n"
            result = result + PrimeraSizer.GetSupportedModelFromDrives(ssdSize, diskCount)
            result = result + "\n"

        return TextSendMessage(text=result)
        #, quick_reply=quickReply)

    @staticmethod
    def GenerateExampleCarousel(title):
        title = title
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
            columnList.append(CarouselColumn(text='Usage\nsize primera [required usable] [TB/TiB]\nPage '+str(i+1), title=title, actions=actions))
        carousel_template = CarouselTemplate(columns=columnList)
        carousel = TemplateSendMessage(
            alt_text='Sizing Wizard support only on Mobile',
            template=carousel_template
        )
        return carousel

    @staticmethod
    def GeneratePrimeraSizer(words):
        if len(words) == 2:
            return PrimeraSizer.GenerateExampleCarousel("Primera Sizer Example")
        elif len(words) == 3:
            required = 0.0
            try:
                required = float(words[2])
            except ValueError:
                return PrimeraSizer.GenerateExampleCarousel("Please input capacity between 0 and 2721") 
            if required <= 0 or required > 2721.29:  
                return PrimeraSizer.GenerateExampleCarousel("Please input capacity between 0 and 2721") 
            return PrimeraSizer.GeneratePrimeraSizeAnswers(unit = "TB", required = required)
        elif len(words) > 3:
            required = 0.0
            try:
                required = float(words[2])
            except ValueError:
                return PrimeraSizer.GenerateExampleCarousel("Please input capacity between 0 and 2721") 
            if required <= 0 or required > 2721.29:  
                return PrimeraSizer.GenerateExampleCarousel("Please input capacity between 0 and 2721") 
            #Check if unit is tb or tib
            unit = words[3].lower()
            unitCheck = ["tb","tib", "gb", "gib", "pb", "pib"]
            if unit not in unitCheck:
                return PrimeraSizer.GenerateExampleCarousel("Please input unit as TB or TiB") 
            return PrimeraSizer.GeneratePrimeraSizeAnswers(unit = unit, required = required)




        