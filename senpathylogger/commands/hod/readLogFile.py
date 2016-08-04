# Written By Mohit Daga, CSE Dept. IIT Madras
# For PG Senpathy Computer Center,IIT Madras
# mohit@cse.iitm.ac.in

from resources.department import *
from numpy import *
from dayStructure import DayStructure
import re

def readLogFile(fname, about="OUT:", hosts={}):
    logs = []
    firstTimeStampArrived = False
    currentDayStructure = DayStructure()
    soft_ID = None
    with open(fname) as f:
        for line in f:
            b=line.strip().split()
            # Two cases of line types
            #1: Line Type this
            ## '0:04:48 (ABAQUSLM) TIMESTAMP 10/19/2013'
            ## b = ['0:04:48', '(ABAQUSLM)', 'TIMESTAMP', '10/19/2013']
            ## date is in mm/dd/yyyy format
            if size(b)>3 and b[2]=="TIMESTAMP":
                newDate = b[3].split('/')
                newDate = map(int,newDate)
                if (firstTimeStampArrived):
                    ## TimeStamp appears but it is equal to the previous
                    if newDate[1] == int(currentDate[1]) and newDate[0] == int(currentDate[0]) and \
                                    newDate[2] == int(currentDate[2]):
                        continue
                    ## New Date has come
                    else :
                        #append currentDayStructure
                        logs.append(currentDayStructure)
                        #Create new currentDayStructure
                        currentDate = newDate
                        currentDayStructure = DayStructure()
                        currentDayStructure.setDate(currentDate[1],currentDate[0],currentDate[2])
                else :
                    firstTimeStampArrived = True
                    currentDate = newDate
                    currentDayStructure.setDate(currentDate[1], currentDate[0], currentDate[2])
            #2:Line Type this
            ## '13:53:50 (ABAQUSLM) OUT: "standard" saran@Z600WS-PC  (5 licenses) '
            ## b = ['13:53:50', '(ABAQUSLM)', 'OUT:', '"standard"', 'saran@Z600WS-PC', '(5', 'licenses)']
            if size(b) > 3 and b[2] == about:
                hostname = b[4]
                departmentInitial = getDepartmentInitial(hostname)
                if departmentInitial:
                    currentDayStructure.incDeptCount(departmentInitial)
                elif getDepartmentFromHostName(hostname, hosts) :
                    currentDayStructure.incDeptCount(getDepartmentFromHostName(hostname,hosts))
                else:
                    currentDayStructure.incDeptCount("unrec")
                    continue
                soft_ID = b[1][1:-1]
    return logs, soft_ID

def getDepartmentInitial(hostname):
    hostname.capitalize().swapcase()
    m = re.match("(ae|am|bs|bt|ce|ch|cs|cy|ed|ee|ep|hs|ma|me|mm|ms|oe|ph|na|pe)[0-9][0-9](s|m|b|d)[0-9][0-9][0-9]",hostname)
    if m:
        m = m.groups()
        return m[0]
    return m

def getDepartmentFromHostName(hostname, hosts):
    hostname = hostname.split("@")[0]
    if hostname in hosts.keys():
        return hosts[hostname].lower()
    else:
        return None