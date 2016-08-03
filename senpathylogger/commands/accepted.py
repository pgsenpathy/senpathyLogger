# Written By Mohit Daga, CSE Dept. IIT Madras
# For PG Senpathy Computer Center,IIT Madras
# mohit@cse.iitm.ac.in

from json import dumps
from .base import Base
import os, sys
from hod.readLogFile import *
from hod.getFilesFromFolder import getLogFilesFromFolder
from hod.generateDeptStats import generateDeptStats
from hod.parseHostFile import parseHostFile

class Accepted(Base):
    """Say hello, world!"""

    def run(self):
        #ToDo: do option checking for

        # Parse OUT FOLDER
        if self.options["--out"] and os.path.exists(self.options["--out"]):
            outPath = os.path.abspath(self.options["--out"])
        else:
            sys.stderr.write("Note: out path not specified, using accepted_stats\n")
            outPath = os.path.abspath("accepted_stats")
            try :
                os.mkdir(outPath)
            except OSError as err:
                if err.errno == 17:
                    sys.stderr.write("Note: accepted_stats already exists. This might overwrite.\n")
                else:
                    sys.exit(err.message)

        # Parse Logs Path
        logsPath = self.options["--logs"]
        if not os.path.exists(logsPath):
            sys.exit("ERR : Specified logs path doesn't exist")
        if not os.path.isabs(logsPath):
            logsPath = os.path.abspath(logsPath)

        logFileList = getLogFilesFromFolder(logsPath)

        if logFileList.__len__() == 0:
            sys.exit("ERR : The specified log folder (--logs) doesnot have have log files\n")

        # Parse host file
        depthosts = {}
        hostfileName = os.path.abspath(self.options["--host"])
        if os.path.exists(hostfileName):
            hosts = parseHostFile(hostfileName)
        else:
            sys.exit("ERR : Specified Host file doesn't exist\n")

        # For Accepted Logs
        acceptedOutPath = outPath + "/accepted"
        try:
            os.mkdir(acceptedOutPath)
        except OSError as err:
            sys.exit(err.message)

        acceptedLogs = {}
        for f in logFileList:
            logs, soft_ID = readLogFile(logsPath + "/" + f, "OUT", hosts)
            if soft_ID:
                if not acceptedLogs.has_key(soft_ID):
                    acceptedLogs.update({soft_ID:[]})
                    acceptedLogs[soft_ID].extend(logs)

        generateDeptStats(acceptedLogs, acceptedOutPath)
        #generateToolWiseStats(acceptedLogs, acceptedOutPath, )

        # Write Code for department wise data denied data
        deniedLogs = {}




