import random
from computadora.Ram import Ram
from computadora.Disk import Disk

class Random:

    def __init__(self):
        self.setRam(Ram())
        self.setDisk(Disk())
        self.setExecTime(0)
        self.setState({})
        self.setThrashingTime(0)
    
    # GETTERS
    def getRam(self):
        return self.__ram

    def getDisk(self):
        return self.__disk

    def getExecTime(self):
        return self.__execTime

    def getThrashingTime(self):
        return self.__thrashingTime

    def getState(self):
        return self.__state


    # SETTERS
    def setRam(self, ram):
        self.__ram = ram

    def setDisk(self, disk):
        self.__disk = disk

    def setExecTime(self, execTime):
        self.__execTime = execTime

    def setThrashingTime(self, thrashingTime):
        self.__thrashingTime = thrashingTime

    def setState(self, state):
        self.__state = state


    # FUNCTIONS
    def addState(self,key,value):
        tempDic = self.getState()
        tempDic[key] = value
        self.setState(tempDic)
    
    def rmvState(self, key):
        tempDic = self.getState()
        del(tempDic[key])
        self.setState(tempDic)

    def removeFromRam(self, page):
        self.addExecTime(1)
        self.getRam().removePage(page)

    def allocateInRam(self, page, pid):
        self.addExecTime(1)
        self.getRam().allocatePage(page)
        data = [page, pid, True, page, self.getRam().getMemory().index(page), -1, self.getExecTime(), False]
        self.addState(page, data)

    def removeFromDisk(self, page):
        self.addExecTime(5)
        self.addThrashingTime(5)
        self.getDisk().removePage(page)

    def allocateInDisk(self, page, pid):
        self.addExecTime(5)
        self.addThrashingTime(5)
        self.getDisk().allocatePage(page)
        data = [page, pid, False, page, -1, self.getDisk().getMemory().index(page), self.getExecTime(), False]
        self.addState(page, data)

    def addExecTime(self, time):
        tempExecTime = self.getExecTime()
        tempExecTime += time
        self.setExecTime(tempExecTime)

    def addThrashingTime(self, time):
        tempTime = self.getThrashingTime()
        tempTime += time
        self.setThrashingTime(tempTime)
    
    def delPag(self, page):
        None

    def allocate(self, newPage, pid):
        if self.getRam().isFull() and newPage not in self.getRam().getMemory():
            if 0 in self.getRam().getMemory():
                if(newPage in self.getDisk().getMemory()):
                    self.removeFromDisk(newPage)
                    #time.sleep(5)
                self.allocateInRam(newPage, pid)
            else:
                page2Remove = random.choice(self.getRam().getMemory())
                self.removeFromRam(page2Remove)
                if(newPage in self.getDisk().getMemory()):
                    self.removeFromDisk(newPage)
                    #time.sleep(5)
                self.allocateInRam(newPage, pid)
                self.allocateInDisk(page2Remove, pid)
        elif newPage not in self.getRam().getMemory():
                self.allocateInRam(newPage, pid)