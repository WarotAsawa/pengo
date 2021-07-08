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