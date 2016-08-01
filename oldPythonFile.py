## Gives output from whatever data is available from different log files
#-----file_name_here------------#

hstFile='hostnames.txt'
depFile='Departments.txt'

#--------headers---------------#
import os
import shutil
from matplotlib.pyplot import *
from numpy import *

#----------Seperate OUT: Data--------------#
# ToDo: Consolidate this to a new file
# Usage of this function
# Give fileName
# Outputs
def junk2data(fname):
    Mnths=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    cMnth=13
    ftarget=[] # Will contain a bunch of file names where the target outputs are stored
    tMnths=[] # Output variable
    tYears=[] # Output variable
    tMnths.append('BFT')
    tYears.append('BFT')
    ftarget.append(fname+'_Data')
    target=open(ftarget[0],'w')
    with open(fname) as f:
        for line in f:
            b=line.strip().split()
            # Two cases of line types
            #1: Line Type this
            ## '0:04:48 (ABAQUSLM) TIMESTAMP 10/19/2013'
            ## b = ['0:04:48', '(ABAQUSLM)', 'TIMESTAMP', '10/19/2013']
            ## date is in mm/dd/yyyy format
            if size(b)>3 and b[2]=="TIMESTAMP" and cMnth!=int(b[3][0:b[3].index('/')]):
                target.close()
                ## Get the month from the date
                cMnth=int(b[3][0:b[3].index('/')])
                ## Get the months (eg 1--> Jan) in alphabetical
                tMnths.append(Mnths[int(b[3][0:b[3].index('/')])-1])
                ## Get the new target file name
                ## This is similar to fname+'_Data_'+ (Month eg 'Jan') + YYYY
                new_file=fname+'_Data_'+Mnths[int(b[3][0:b[3].index('/')])-1]+'_'+b[3][b[3].rfind('/')+1:]
                ## Add the year to the file
                tYears.append(b[3][b[3].rfind('/')+1:])
                ## open the new target file
                target=open(new_file,'w')
                ## Add the target file to the output variable fTarget
                ftarget.append(new_file)
            #2:Line Type this
            ## '13:53:50 (ABAQUSLM) OUT: "standard" saran@Z600WS-PC  (5 licenses) '
            ## b = ['13:53:50', '(ABAQUSLM)', 'OUT:', '"standard"', 'saran@Z600WS-PC', '(5', 'licenses)']
            if size(b)>3 and b[2]=="OUT:":
                if size(b)>5:
                    for x in range(5,size(b)):
                        b[4]=b[4]+b[x]
                for i in range(5):
                    target.write(str(b[i])+'\t')
                target.write('\n')
                soft_ID=b[1]
                soft_ID=soft_ID[1:len(soft_ID)-1] #eg ABAQUSLM in the above case
    target.close()
    return soft_ID,ftarget,tMnths,tYears

#------------ Toolbox data------------------#
def toolbox_stat(cDir,fData,soft_ID):
    with open(soft_ID+'_Toolboxes.txt') as f:
        for line in f:
           toolbox=line.strip().split()
    toolbox_count=zeros(size(toolbox));
    with open(fData) as f:
        for line in f:
            b=line.strip().split()
            toolbox_count[toolbox.index(b[3])]+=1
    target=cDir+'/'+soft_ID+'_toolbox_data.txt'
    toolboxdata=open(target,'w')
    for j in range(size(toolbox)):
        toolboxdata.write(toolbox[j]+'\t'+str(toolbox_count[j])+'\n')
    figure()
    h = bar(xrange(len(toolbox)), toolbox_count, label=toolbox)
    subplots_adjust(bottom=0.3)
    xticks_pos = [0.65*patch.get_width() + patch.get_xy()[0] for patch in h]
    xticks(xticks_pos, toolbox,  ha='right', rotation=90)
    savefig(cDir+'/'+soft_ID+'_toolbox_stat.png',bbox_inches='tight', pad_inches=0.5)
    close()
    toolboxdata.close()
    return toolbox_count

#---------- Read Hostname and Host Department --------#
# ToDo: Consolidate : To a different folder
# Output
# hstname (array)
# hstdept (department)
def rHstname(fName):
    hstname=[]
    hstdept=[]
    with open(fName) as f:
        for line in f:
           hname=line.strip().split()
           if size(hname)>2:
               for i in range(2,size(hname)):
                   hname[1]=hname[1]+hname[i]
           hstname.append(hname[1])
           hstdept.append(hname[0])
    return hstname,hstdept

#---------- Read Hostname and Host Department --------#
# ToDo: Consolidate : To a different folder
# Output department name
def rDept(fName):
    with open(fName) as f:
        for line in f:
           department=line.strip().split()
    return department

#----------- Department Statistics ----------------#
# ToDo: Consolidate this to a new file
## deptStat
## Input :
# mcDir : eg ABAQUSLM/2013/Oct
# fData[months] : name of the file name corrosponding with the month
# hstname : hstnames information
# department : list of department initials like CS,CE etc.
# soft_ID : ABAQUSLM
def deptStat(cDir,fData,hstname,hstdept,department,soft_ID):
    chars = set('0123456789')
    department_count=zeros(size(department));
    fdepartment_target=[]
    Unrecognized_count=0
    fUnrecognized=cDir+'/'+soft_ID+'_Unrecognized.txt'
    open_Unrecognized=open(fUnrecognized,'w')
    for i in department:
       fdepartment=cDir+'/'+soft_ID+'_'+i+'.txt'
       open_department=open(fdepartment,'w')
       fdepartment_target.append(open_department)
    with open(fData) as f:
        for line in f:
            line_found=0
            b=line.strip().split()
            if (b[4].upper()[0:2] in department) and (b[4][2] in chars):
                line_found=1
                i=department.index(b[4].upper()[0:2])
                department_count[i]+=1
                for j in range(size(b)):
                    fdepartment_target[i].write(str(b[j])+'\t')
                fdepartment_target[i].write('\n')
            if (line_found==0) and (b[4][b[4].index('@')+1:] in hstname):
               line_found=1
               sample=b[4][b[4].index('@')+1:]
               department_count[department.index(hstdept[hstname.index(sample)])]+=1
               for j in range(size(b)):
                   fdepartment_target[department.index(hstdept[hstname.index(sample)])].write(str(b[j])+'\t')
               fdepartment_target[department.index(hstdept[hstname.index(sample)])].write('\n')
            if (line_found==0):
               Unrecognized_count+=1
               for j in range(size(b)):
                  open_Unrecognized.write(str(b[j])+'\t')
               open_Unrecognized.write('\n')
    for i in fdepartment_target:
       i.close()
    open_Unrecognized.close()
    departmentdata=open(cDir+'/'+soft_ID+'_department_data.txt','w')
    for j in range(size(department)):
        departmentdata.write(department[j]+'\t'+str(department_count[j])+'\n')
    departmentdata.close()
    figure()
    h = bar(xrange(len(department)), department_count, label=department)
    subplots_adjust(bottom=0.3)
    xticks_pos = [0.65*patch.get_width() + patch.get_xy()[0] for patch in h]
    xticks(xticks_pos, department,  ha='right', rotation=90)
    savefig(cDir+'/'+soft_ID+'_department_stat.png',bbox_inches='tight', pad_inches=0.5)
    close()
    return department_count, Unrecognized_count

#----------- Read Data ----------------#
def rData(fname,soft_ID,cDIR,sMonth,sYear,eMonth,eYear,department):
    Mnths=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    department_count=zeros(size(department))
    with open(soft_ID+'_Toolboxes.txt') as f:
        for line in f:
           toolbox=line.strip().split()
    toolbox_count=zeros(size(toolbox));
    for yr in range(eYear-sYear+1):
        if yr==0:
            j=sMonth-1;
        else:
            j=0;
        if yr==eYear-sYear:
            k=eMonth
        else:
            k=12;
        for mnt in range(j,k):
            mcDir=cDir+'/'+str(sYear+yr)+'/'+Mnths[mnt]
            if os.path.exists(mcDir):
                filename=mcDir+'/'+soft_ID+'_department_data.txt'
                with open(filename) as f:
                    counter=0
                    for line in f:
                        b=line.strip().split()
                        department_count[counter]+=float(b[1])
                        counter+=1
                filename=mcDir+'/'+soft_ID+'_toolbox_data.txt'
                with open(filename) as f:
                    counter=0
                    for line in f:
                        b=line.strip().split()
                        toolbox_count[counter]+=float(b[1])
                        counter+=1
            else:
                print 'Data for ' + Mnths[mnt] +' '+ str(sYear+yr) + ' is unavailable.'
    for j in range(size(department)):
        print str(department[j])+'\t'+str(department_count[j])
    for j in range(size(toolbox)):
        print str(toolbox[j])+'\t'+str(toolbox_count[j])
    figure()
    h = bar(xrange(len(department)), department_count, label=department)
    subplots_adjust(bottom=0.3)
    xticks_pos = [0.65*patch.get_width() + patch.get_xy()[0] for patch in h]
    xticks(xticks_pos, department,  ha='right', rotation=90)

    figure()
    h = bar(xrange(len(toolbox)), toolbox_count, label=toolbox)
    subplots_adjust(bottom=0.3)
    xticks_pos = [0.65*patch.get_width() + patch.get_xy()[0] for patch in h]
    xticks(xticks_pos, toolbox,  ha='right', rotation=90)
    return department_count,toolbox_count

#---------- Program Starts here ------------#
#---------- Ask for file name and months --------#
# Todo : MD Consolidate it to a new file. takes the input and returns 5 variables
# FileName, Start Month, Start Year, End Month. End Year
fname=raw_input('Enter a file name: ')
while(1):
    try:
        sMonth=int(raw_input('Enter starting Month (Jan=1;Dec=12): '))
    except ValueError:
        continue
    else:
        if sMonth>12 or sMonth<1:
            continue
        else:
            break
while(1):
    try:
        sYear=int(raw_input('Enter starting Year (1900-2100): '))
    except ValueError:
        continue
    else:
        if sYear>2100 or sYear<1900:
            continue
        else:
            break
while(1):
    try:
        eMonth=int(raw_input('Enter ending Month (Jan=1;Dec=12): '))
    except ValueError:
        continue
    else:
        if eMonth>12 or eMonth<1:
            continue
        else:
            break
while(1):
    try:
        eYear=int(raw_input('Enter ending Year (1900-2100): '))
    except ValueError:
        continue
    else:
        if eYear>2100 or eYear<1900:
            continue
        else:
            break

## Main Porgram
## ToDo: Consolidate it to a new file Main File

# Takes the path of this file
cDir=os.path.dirname(os.path.realpath(__file__))

# Calls junk2Data Reads all the data from the log file and returns
# SoftID (a string) : Software Id eg 'ABAQUSLM' in the above case
# fData  (an array) : Files created by the tool
# tMnths (an array) : Month for each file, starts with BFT (before seeing a timestamp) eg. = ['BFT', 'Oct']
# tYears (an array) : Year for each file, starts with BFT (before seeing a timestamp) eg. = ['BFT', '2013']

soft_ID, fData,tMnths,tYears=junk2data(fname)
cDir=cDir+'/'+soft_ID
# Create a new directory of not already exists eg. ABAQUSLM
if not os.path.exists(cDir):
    os.makedirs(cDir)
# months are just indixes in the next array
for months in range(size(tMnths)):
    mcDir=cDir+'/'+tYears[months]+'/'+tMnths[months]
    # Makes a new directory of the form ABAQUSLM/2013/Oct
    if not os.path.exists(mcDir):
        os.makedirs(mcDir)
    # Get toolbox stats
    toolbox_count=toolbox_stat(mcDir,fData[months],soft_ID)
    # read hostname files
    # Should be taken out of the loop
    hstname,hstdept=rHstname(hstFile)
    # read department file
    # Should be taken out of the loop
    department=rDept(depFile)
    department_count, Unrecognized_count=deptStat(mcDir,fData[months],hstname,hstdept,department,soft_ID)
    print 'Total Recognized Deparmental User = '+str(sum(department_count))
    print 'Unrecognized Users = '+str(Unrecognized_count)
    shutil.move(fData[months], mcDir+'/'+fData[months])
#------- Reading and Displaying Data ------#
if sMonth > 12 or sMonth < 1 or eMonth > 12 or eMonth < 1 or sYear > 2100 or sYear<1900 or eYear<1900 or eYear>2100:
    print 'Invalid Date Selection'
else:
    department_count,toolbox_count=rData(fname,soft_ID,cDir,sMonth,sYear,eMonth,eYear,department)
    show()
