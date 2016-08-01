from resources.department import *
import datetime
import sys

class DayStructure:
    def __init__(self):
        self.depts = {}
        map(lambda k: self.depts.update({k: 0}), departmentInitials)
        self.depts["unrec"] = 0 #unrecognized
        self.__dict__["date"] = None

    def incDeptCount(self, deptInitial):
        if deptInitial== "na" or deptInitial == "pe":
            deptInitial = "oe"
        if deptInitial == "unrec":
            self.depts["unrec"] += 1
        elif deptInitial in departmentInitials:
            self.depts[deptInitial] += 1
        else:
            print deptInitial
            sys.exit("ERR : wrong department initial update in day structure")

    def setDate(self, dd, mm, yyyy):
        self.__dict__["date"] = datetime.date(yyyy, mm, dd)

    def getMonth(self):
        if (self.__dict__["date"]):
            return self.__dict__["date"].month

    def sameMonth(self, other):
        return self.getYear() == other.getYear() and self.getMonth() == other.getMonth()

    def sameYear(self,other):
        return self.getYear() == other.getYear()

    def getYear(self):
        if (self.__dict__["date"]):
            return self.__dict__["date"].year

    def getday(self):
        if (self.__dict__["date"]):
            return self.__dict__["date"].day

    def setDateD(self,date):
        self.__dict__["date"] = date

    def __eq__(self, other):
        return self.__dict__["date"] == other.__dict__["date"]

    def __ge__(self, other):
        return self.__dict__["date"] >= other.__dict__["date"]

    def __gt__(self, other):
        return self.__dict__["date"] > other.__dict__["date"]

    def __le__(self, other):
        return self.__dict__["date"] <= other.__dict__["date"]

    def __lt__(self, other):
        return self.__dict__["date"] < other.__dict__["date"]

    def __repr__(self):
        return self.__dict__["date"].isoformat() + " " + repr(self.depts) + "\n"

    def __add__(self, other):
        for key in self.depts.keys():
            self.depts[key] += other.depts[key]
        return self

    def __sub__(self, other):
        return self.__dict__["date"] - other.__dict__["date"]

    def getDepartments(self):
        return self.depts.keys()

    def getDepartmentCount(self):
        return self.depts.values()

    def getMonthName(self):
        return self.__dict__["date"].strftime('%B') + str(self.getYear())

    def getWeekName(self):
        return self.__dict__["date"].isoformat()