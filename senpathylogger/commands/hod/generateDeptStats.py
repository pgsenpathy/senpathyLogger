# Written By Mohit Daga, CSE Dept. IIT Madras
# For PG Senpathy Computer Center,IIT Madras
# mohit@cse.iitm.ac.in

import os, sys
import datetime
from dayStructure import DayStructure
from matplotlib.pyplot import *
from addMonths import add_months

def generateDeptStats(structuredLogs, outPath, weekly=True, monthly=False, yearly=False):
    ## Find different soft id of
    # Remove all the log enteries which do not none as
    ## Sort the log
    for toolbox in structuredLogs.keys():
        structuredLogs[toolbox].sort()
        folderPath = outPath + "/" + toolbox
        ## Do some sanity check
        try:
            os.mkdir(folderPath)
        except OSError as err:
            if err.errno == 13:
                sys.exit("ERR : Do not have permission to use the out folder\n")
        #1. Write the logs in a file
        f = open(folderPath+"/rawstats.log", "w")
        for k in structuredLogs[toolbox]:
            f.write(k.date.isoformat() + " " + repr(k) + "\n")
        f.close()

        #2. Create a weekly graphs
        # Department Stats weekly, monthly, yearly for toolbox
        weeklyDepartmentStats(structuredLogs[toolbox], toolbox, folderPath)
        monthlyDepartmentStats(structuredLogs[toolbox], toolbox, folderPath)
        yearlyDepartmentStats(structuredLogs[toolbox], toolbox, folderPath)

        #3 Create a monthly graph
        ##a monthly for toolbox
        ##b monthly for departments

        #4 create a annual graph
        ##a for toolbox
        ##b for departments


    ## Make weekly graph
    ## Make monthly graph
    ## Make yearly graph
    return "smth"

def weeklyDepartmentStats(logs, toolbox, outPath ,startDate = None):
    if startDate==None:
        firstDayStructure = min(logs)
        startDate = firstDayStructure.date
    lastDateDayStructure = max(logs)
    lastDate = lastDateDayStructure.date
    index = 0
    folderPath = outPath + "/" + "weekly"
    try:
        os.mkdir(folderPath)
    except OSError as err:
        if err.errno == 13:
            sys.exit("ERR : Do not have permission to use the out folder\n")
    weeklyTarget = open(folderPath+"/weeklyraw.log","w")
    for i in range(0, 1 + ((lastDate-startDate)/7).days):
        thisWeekStructure = DayStructure()
        thisWeekStructure.setDateD(startDate + datetime.timedelta(7*i))
        while logs.__len__()>index and (logs[index]-thisWeekStructure).days < 7:
            thisWeekStructure += logs[index]
            index += 1
        weeklyTarget.write(repr(thisWeekStructure))
        saveDepartmentStatistics(thisWeekStructure, folderPath + "/" + thisWeekStructure.getWeekName() + ".png")
    weeklyTarget.close()

def monthlyDepartmentStats(logs, toolbox, outPath ,startDate = None):
    if startDate==None:
        firstDayStructure = min(logs)
        startDate = firstDayStructure
    lastDateDayStructure = max(logs)
    lastDate = lastDateDayStructure
    index = 0
    folderPath = outPath + "/" + "monthly"
    try:
        os.mkdir(folderPath)
    except OSError as err:
        if err.errno == 13:
            sys.exit("ERR : Do not have permission to use the out folder\n")
    monthlyTarget = open(folderPath+"/monthlyraw.log", "w")
    for i in range(0, 1 + lastDate.getMonth()-startDate.getMonth() + 12 * (lastDate.getYear()-startDate.getYear())):
        thisMonthStructure = DayStructure()
        thisMonthStructure.setDateD(add_months(datetime.date(startDate.getYear(), startDate.getMonth(), 1), i))
        print i, index, logs.__len__(), logs[index]
        while logs.__len__()>index and logs[index].sameMonth(thisMonthStructure):
            thisMonthStructure += logs[index]
            index += 1
        monthlyTarget.write(repr(thisMonthStructure))
        saveDepartmentStatistics(thisMonthStructure, folderPath + "/"  + thisMonthStructure.getMonthName() + ".png")
        # ToDo: some fancy states
    monthlyTarget.close()

def yearlyDepartmentStats(logs, toolbox, outPath ,startDate = None):
    if startDate==None:
        firstDayStructure = min(logs)
        startDate = firstDayStructure
    lastDateDayStructure = max(logs)
    lastDate = lastDateDayStructure
    index = 0
    folderPath = outPath + "/" + "yearly"
    try:
        os.mkdir(folderPath)
    except OSError as err:
        if err.errno == 13:
            sys.exit("ERR : Do not have permission to use the out folder\n")
    yearlyTarget = open(folderPath+"/yearlyraw.log", "w")
    for i in range(0, 1 + (lastDate.getYear()-startDate.getYear())):
        thisYearStructure = DayStructure()
        thisYearStructure.setDate(1, 1, startDate.getYear() + i)
        print i, index, logs.__len__(), logs[index]
        while logs.__len__()>index and logs[index].sameYear(thisYearStructure):
            thisYearStructure += logs[index]
            index += 1
        yearlyTarget.write(repr(thisYearStructure))
        saveDepartmentStatistics(thisYearStructure,folderPath + "/" + str(thisYearStructure.getYear()) + ".png")
    yearlyTarget.close()

def saveDepartmentStatistics(dayStructure, imagePath):
    department = dayStructure.getDepartments()
    department_count = dayStructure.getDepartmentCount()
    figure()
    h = bar(xrange(len(department)), department_count, label=department)
    subplots_adjust(bottom=0.3)
    xticks_pos = [0.65*patch.get_width() + patch.get_xy()[0] for patch in h]
    xticks(xticks_pos, department,  ha='right', rotation=90)
    savefig(imagePath, bbox_inches='tight', pad_inches=0.5)
    close()
    return "smth"