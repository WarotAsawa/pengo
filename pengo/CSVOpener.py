import csv;
import os;

class CSVOpener:
    #CSV Path
    csvPath = './data/'
    
    #Create 2D Array from CSV File
    @staticmethod
    def GetArrayFromCSV(fileName):
        with open(fileName, newline='') as f:
            reader = csv.reader(f)
            data = list(reader)
            return data
    #Search and Open CSV from root
    @staticmethod
    def SearchAndOpenCSV(fileName):
        fileName = fileName.strip().lower()
        dirList = os.listdir(CSVOpener.csvPath)
        for dir in dirList:
            fileList = os.listdir(CSVOpener.csvPath+dir+'/')
            for file in fileList:
                if fileName.split('.')[1] != 'csv': continue
                targetName = file.split('.')[0]
                if fileName == targetName.lower():
                    return CSVOpener.GetArrayFromCSV(CSVOpener.csvPath+dir+'/'+targetName+'.csv')
        return ["Can not find searched file"]

