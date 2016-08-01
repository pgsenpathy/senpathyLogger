# Written By Mohit Daga, CSE Dept. IIT Madras
# For Computer Center,IIT Madras
# mohit@cse.iitm.ac.in

from os import listdir

def getLogFilesFromFolder(folderName, ext=".log"):
    results = []
    for f in listdir(folderName):
        if f.endswith(ext):
            results.append(f)
    return results