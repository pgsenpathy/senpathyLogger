# Written By Mohit Daga, CSE Dept. IIT Madras
# For PG Senpathy Computer Center,IIT Madras
# mohit@cse.iitm.ac.in

from json import dumps
from .base import Base
import os, sys
from hod.readLogFile import *
from hod.getFilesFromFolder import getLogFilesFromFolder
from hod.generateStats import generateStates

class Some(Base):
    """Say hello, world!"""

    def run(self):
        print "I was here thank god"