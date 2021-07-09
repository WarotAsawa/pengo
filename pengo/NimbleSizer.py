import math
import random
from AllResponse import AllResponse

from linebot.models import (
    TextSendMessage, QuickReplyButton, MessageAction , TemplateSendMessage, CarouselTemplate, CarouselColumn, QuickReply
)
from Converter import Converter
from LineConst import LineConst
from ImageConst import ImageConst
from CSVOpener import CSVOpener

class NimbleES3Shelf():
    hddSize = 1
    ssdCache = []
    def __init__(self, hddSize):
        self.hddSize = hddSize

    def SetHDDSize(self, hddSize):
        self.hddSize = hddSize

    def AddSSDCache(self, ssdSize, amount = 1):
        if len(self.ssdCache) + amount < 6:
            for i in range(0,amount):
                self.ssdCache.append(ssdSize)

class NimbleHFArray():
    shelfList = [NimbleES3Shelf]
    rawCapacity = 0
    cacheCapacity = 0
    usableCapacity = 0
    def __init__(self):
        return "Nimble is craeted"
    
    @staticmethod
    def GetUsableFromRaw(self,raw):
        if raw == 21: return 16.31
        elif raw == 42: return 33.27
        elif raw == 84: return 67.21
        elif raw == 126: return 101.14
        elif raw == 210: return 169
        elif raw == 294: return 236.39
        else: return 0

    def AddShelf(self, hddSize):
        NewShelf = NimbleES3Shelf(hddSize)
        if len(self.shelfList) == 0:
            #Insert First Shelf SSD
            if hddSize == 1: NewShelf.AddSSDCache(0.48,6); 
            if hddSize == 2: NewShelf.AddSSDCache(0.96,6); 
            if hddSize == 4: NewShelf.AddSSDCache(0.96,3); NewShelf.AddSSDCache(1.92,3); 
            if hddSize == 6: NewShelf.AddSSDCache(3.84,3); NewShelf.AddSSDCache(1.92,3)
            if hddSize == 10: NewShelf.AddSSDCache(3.84,6)
            if hddSize == 14: NewShelf.AddSSDCache(7.68,6)
        elif len(self.shelfList) < 7:
            if hddSize == 1: NewShelf.AddSSDCache(0.48,3); 
            if hddSize == 2: NewShelf.AddSSDCache(0.96,3); 
            if hddSize == 4: NewShelf.AddSSDCache(1.92,3)
            if hddSize == 6: NewShelf.AddSSDCache(3.84,2); NewShelf.AddSSDCache(1.92,1);
            if hddSize == 10: NewShelf.AddSSDCache(3.84,3); NewShelf.AddSSDCache(1.92,3);
            if hddSize == 14: NewShelf.AddSSDCache(7.68,3);
        
        self.shelfList.append(NewShelf)
        self.ResetCapacity()

        fdr = self.cacheCapacity / self.rawCapacity
        #If FDR < 12 then add Minimum SSD
        if fdr < 12:
            ssdSizeList =  [0.96,1.92,3.84,7.68]
            #Add More SSD
            for ssdSize in ssdSizeList:
                if (self.cacheCapacity + 3*ssdSize) / self.rawCapacity >= 12:
                    lastShelf = self.shelfList[len(self.shelfList)-1]
                    lastShelf.AddSSDCache(ssdSize,3)

        self.ResetCapacity()

    def ResetCapacity(self):
        totalHDD = 0
        totalSSD = 0
        totalUsable = 0
        for shelf in self.shelfList:
            totalHDD += shelf.hddSize * 21
            totalUsable = self.GetUsableFromRaw(self,shelf.hddSize * 21)
            for ssd in shelf.ssdCache:
                totalSSD += ssd
        self.rawCapacity = totalHDD
        self.cacheCapacity = totalSSD
        self.usableCapacity = totalUsable

    def GetAllSupportedModel(self):
        self.ResetCapacity;
        result = ""
        if self.rawCapacity <= 210 and self.cacheCapacity <= 28:
            result = result + "HF20 "
        if self.rawCapacity <= 504 and self.cacheCapacity <= 60:
            result = result + "HF40 "
        if self.rawCapacity <= 1260 and self.cacheCapacity <= 156:
            result = result + "HF60 "
        return result

class NimbleSizer:

    @staticmethod
    def HFSizer(requiredTB):
        #set result
        resultArray = NimbleHFArray()
        diskSizeList = [14,10,6,4,2,1]
        for i in range (0,7):
            for diskSize in diskSize:
                addedUsable =  NimbleHFArray.GetUsableFromRaw(diskSize * 21)
                #Check if sizing too Big
                if resultArray.usableCapacity + addedUsable - requiredTB > 31:
                    #Check if exceed capacity is worth a shelf. Except for last shelf
                    if i < 6: continue
                resultArray.AddShelf(diskSize)
                break
        return resultArray

    @staticmethod
    def GenerateNimbleSizerAnswers(unit = "TB", required = 50.0, model = "HF"):
        multiplier = Converter.TBToUnitMultipler(unit)
        convertedRequired = required * multiplier
        result = AllResponse.GetRandomResponseFromKeys('preAnswer')

        #Set Quick reply for convert unit (TB,TiB) and offer 100,90% utilization sizing
        buttonList = [];
        TB100 = "TB"
        TiB100 = "TiB"
        TB90 = "TB @90%"
        TiB90 = "TiB @90%"
        strSizing = str(math.floor(required))
        newRand = random.randint(10, 1800)
        #Check if has no answers
        if model == 'AF':
            result = "This feature is not yet implemented. Please try HF Sizing these instead"
            model = 'HF'
        elif model == 'HF':
            resultArray = NimbleSizer.HFSizer(convertedRequired)
            result = result + "Total Raw: " + resultArray.rawCapacity + "TB / " + resultArray.rawCapacity/Converter.TBToUnitMultipler("tib") + " TiB\n"
            result = result + "Total Usable: " + resultArray.usableCapacity + "TB / " + resultArray.usableCapacity/Converter.TBToUnitMultipler("tib") + " TiB\n"
            result = result + "Total SSD Cache: " + resultArray.cacheCapacity + "TB / " + resultArray.cacheCapacity/Converter.TBToUnitMultipler("tib") + " TiB\n"
            result = result + "FDR: " + str(round(resultArray.cacheCapacity/resultArray.usableCapacity*100,2)) + "%"
            count = 0
            for shelf in resultArray.shelfList:
                result = result + "\nShelf " + count + " :\n"
                result = result + "HDD: 21x" + shelf.hddSize + "TB HDD\n"
                result = result + "Cache: "
                allSSD = {}
                for ssd in shelf.ssdCache:
                    if ssd not in allSSD: allSSD[str(ssd)] = 1
                    else: allSSD[str(ssd)] += 1
                for ssd in allSSD.keys():
                    ssdSize = float(ssd)
                    if ssdSize < 1: result = result +  allSSD[ssd] + "x" + str(math.floor(ssdSize*1000)) + "GB"
                    else: result = result +  allSSD[ssd] + "x" + str(ssdSize) + "TB"
                result = result +  "\n"
            if resultArray.GetAllSupportedModel == "":
                result = AllResponse.GetRandomResponseFromKeys('errorWord') + "\nNo answers found !! Try these instead."
                strSizing = str(newRand)
                required = newRand

        buttonList.append(QuickReplyButton(image_url=ImageConst.sizeIcon, action=MessageAction(label=strSizing+TB100, text="size nimble "+ model + str(required)+" TB")))
        buttonList.append(QuickReplyButton(image_url=ImageConst.sizeIcon, action=MessageAction(label=strSizing+TiB100, text="size nimble "+model + str(required)+" TiB")))
        buttonList.append(QuickReplyButton(image_url=ImageConst.sizeIcon, action=MessageAction(label=strSizing+TB90, text="size nimble "+model + str(math.ceil(required/0.9))+" TB")))
        buttonList.append(QuickReplyButton(image_url=ImageConst.sizeIcon, action=MessageAction(label=strSizing+TiB90, text="size nimble "+model + str(math.ceil(required/0.9))+" TiB")))

        quickReply=QuickReply(items=buttonList)

        return TextSendMessage(text=result, quick_reply=quickReply)
        #, quick_reply=quickReply)

    @staticmethod
    def GenerateExampleCarousel(title, mode):
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
            columnList.append(CarouselColumn(text='Usage\nsize nimble [required usable] [TB/TiB]\nPage '+str(i+1), title=title, actions=actions))
        carousel_template = CarouselTemplate(columns=columnList)
        carousel = TemplateSendMessage(
            alt_text='Sizing Wizard support only on Mobile',
            template=carousel_template
        )
        return carousel

    @staticmethod
    def GenerateModelSelection():
        title = "Please Select Nimble Model"
        textPreFix = "size nimble "
        columnList = []
        
        actions = []
        actions.append(MessageAction(label="AF",text=textPreFix + "AF"))
        actions.append(MessageAction(label="HF",text=textPreFix + "HF"))
        columnList.append(CarouselColumn(text='Usage\nsize nimble [AF/HF] [required usable] [TB/TiB]\n', title=title, actions=actions))
        carousel_template = CarouselTemplate(columns=columnList)
        carousel = TemplateSendMessage(
            alt_text='Sizing Wizard support only on Mobile',
            template=carousel_template
        )
        return carousel

    @staticmethod
    def GenerateNimbleSizer(words):
        model = ""
        if len(words) > 2:
            model = words[2].strip().upper()
            if model != 'AF' and model != 'HF':
                return NimbleSizer.GenerateModelSelection()
        
        if len(words) == 2:
            return NimbleSizer.GenerateModelSelection()
        elif len(words) == 3:
            return NimbleSizer.GenerateExampleCarousel("Nimble Sizer Example", model)
        elif len(words) == 4:
            required = 0.0
            try:
                required = float(words[3])
            except ValueError:
                return NimbleSizer.GenerateExampleCarousel("Please input capacity between 0 and 1180", model) 
            if required <= 0 or required > 1180:  
                return NimbleSizer.GenerateExampleCarousel("Please input capacity between 0 and 1180", model) 
            return NimbleSizer.GenerateNimbleSizerAnswers(unit = "TB", required = required, model = model)
        elif len(words) > 4:
            required = 0.0
            try:
                required = float(words[2])
            except ValueError:
                return NimbleSizer.GenerateExampleCarousel("Please input capacity between 0 and 1180") 
            if required <= 0 or required > 1180:  
                return NimbleSizer.GenerateExampleCarousel("Please input capacity between 0 and 1180") 
            #Check if unit is tb or tib
            unit = words[3].lower()
            unitCheck = ["tb","tib"]
            #unitCheck = ["tb","tib", "gb", "gib", "pb", "pib"]
            if unit not in unitCheck:
                return NimbleSizer.GenerateExampleCarousel("Please input unit as TB or TiB") 
            return NimbleSizer.GenerateNimbleSizerAnswers(unit = unit, required = required,model = model)




        