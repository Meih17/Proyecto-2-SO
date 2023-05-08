from computadora.Ram import Ram
from computadora.Disk import Disk

class Optimal:

    def __init__(self, memCalls):
        self.setMemCalls(memCalls)
        self.setRam(Ram())
        self.setDisk(Disk())
        self.setData({})
        self.setExecTime(0)
        self.setState({})
        self.setThrashingTime(0)

    
    # GETTERS
    def getMemCalls(self):
        return self.__memCalls

    def getRam(self):
        return self.__ram

    def getDisk(self):
        return self.__disk

    def getExecTime(self):
        return self.__execTime

    def getData(self):
        return self.__data

    def getThrashingTime(self):
        return self.__thrashingTime

    def getState(self):
        return self.__state

    # SETTERS
    def setMemCalls(self, memCalls):
        self.__memCalls = memCalls

    def setRam(self, ram):
        self.__ram = ram

    def setDisk(self, disk):
        self.__disk = disk

    def setExecTime(self, execTime):
        self.__execTime = execTime
    
    def setData(self,data):
        self.__data = data

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

    def getNextMemCall(self):
        tempQueue = self.getMemCalls()
        element = tempQueue.pop()
        self.setMemCalls(tempQueue)
        return element

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
        
    def allocateNext(self, pid):
        for page in self.getNextMemCall():
            if self.getRam().isFull() and page not in self.getRam().getMemory():
                if 0 in self.getRam().getMemory():
                    if(page in self.getDisk().getMemory()):
                        self.removeFromDisk(page)
                    tim = self.getExecTime()
                    self.allocateInRam(page, pid)
                    lAddr = self.getRam().getMemory().index(page)
                else:
                    restOfMemCalls = self.getMemCalls().getQueue()
                    index = -1
                    marked = [-1, index]
                    for page2Remove in self.getRam().getMemory():
                        found = False
                        for restPage in restOfMemCalls:
                            if page2Remove in restPage:
                                index = restOfMemCalls.index(restPage)
                                found = True
                        if index > marked[1]:
                            marked = [page2Remove, index]
                        if not found:
                            marked = [page2Remove, index]
                            break
                    self.removeFromRam(marked[0])
                    if(page in self.getDisk().getMemory()):
                        self.removeFromDisk(page)
                    tim = self.getExecTime()
                    self.allocateInRam(page, pid)
                    lAddr = self.getRam().getMemory().index(page)
                    self.allocateInDisk(marked[0], pid)
                    timeDisk = self.getExecTime() 
                    pos = self.getDisk().getMemory().index(marked[0])
            elif page not in self.getRam().getMemory():
                tim = self.getExecTime()
                self.allocateInRam(page, pid)
                lAddr = self.getRam().getMemory().index(page)
            