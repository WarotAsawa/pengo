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
class PrimeraSizer:
    #Primera Overhead
    systemOverheadTB = 2.92;

    #Alletra9000 Overhead
    #systemOverhead = 6.22;
    targetUtilization = 0.9;
    #Max Dirve supported each mode
    maxDrive = {}
    maxDrive["A630"] = 144
    maxDrive["A650"] = 384
    maxDrive["A670"] = 576
    #Max Capacity supported each mode
    maxCapacityTB = {}
    maxCapacityTB["A630"] = 250
    maxCapacityTB["A650"] = 1600
    maxCapacityTB["A670"] = 3200

    @staticmethod
    def GetTBUsable(diskSize, diskCount):
        #Defalt R6 size = 10+2 = 12
        raid6SetSize = 12
        spareTB = diskSize * 2
        rawTB = diskSize * diskCount

        #Check drive input
        if diskCount < 8 or diskCount%2 == 1:
            print("Please input diskcount as even number > 8")
            return 0

        #Adjust RAID6 size
        if diskCount < 12: raid6SetSize = diskCount

        #Config Spare
        if diskSize * diskCount * 0.1 > spareTB:
            spareTB = diskSize * diskCount * 0.1;

        usableTB = (rawTB - spareTB - PrimeraSizer.systemOverheadTB) * (raid6SetSize - 2) / raid6SetSize

        return usableTB
    
    @staticmethod
    def SearchDiskCount(diskSize, usableTB):
        #Use Binary Search
        minTBDiff = 3200
        upperDiskPair = 288
        lowerDiskPair = 4
        midDiskPair = 0
        driveResult = 288

        while upperDiskPair > lowerDiskPair:
            midDiskPair = math.ceil((upperDiskPair + lowerDiskPair)/2.0)
            tempUsableTB = PrimeraSizer.GetTBUsable(diskSize, midDiskPair*2)
            if tempUsableTB > usableTB:
                newDiff = tempUsableTB - usableTB
                if newDiff <= minTBDiff:
                    minTBDiff = newDiff
                    driveResult = midDiskPair
                upperDiskPair = midDiskPair - 1
            elif tempUsableTB < usableTB:
                lowerDiskPair = midDiskPair + 1

        return driveResult

    @staticmethod
    def GetSupportedModelFromDrives(diskSize, diskCount):
        rawTB = diskSize * diskCount
        maxDrive = PrimeraSizer.maxDrive
        maxCapacityTB = PrimeraSizer.maxCapacityTB
        result = "Supported Model:"
        allModel = ["A630", "A650", "A670"]
        for model in allModel:
            if diskCount <= maxDrive[model] and rawTB <= maxCapacityTB[model]:
                result = result + " " + model
