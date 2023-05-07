from computadora.Ram import Ram
from computadora.Disk import Disk

class MRU:
    def __init__(self):
        self.setRam(Ram())
        self.setDisk(Disk())
        self.setMemoryAccesses([])
        self.setExecTime(0)
        self.setThrashingTime(0)
        self.setMarked(1)
        self.setState({})
    
    # GETTERS
    def getRam(self):
        return self.__ram

    def getDisk(self):
        return self.__disk
    
    def getMemoryAccesses(self):
        return self.__memoryAccesses

    def getMarked(self):
        return self.__marked

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

    def setMemoryAccesses(self, memoryAccesses):
        self.__memoryAccesses = memoryAccesses

    def setMarked(self, marked):
        self.__marked = marked

    def setExecTime(self, execTime):
        self.__execTime = execTime

    def setRunningTime(self, runningTime):
        self.__runningTime = runningTime

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

    def addMemoryAccess(self, page):
        tempMem = self.getMemoryAccesses()
        tempMem.insert(0, page)
        self.setMemoryAccesses(tempMem)

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

    def allocate(self, newPage, pid):
        if self.getRam().isFull() and newPage not in self.getRam().getMemory():
            if 0 in self.getRam().getMemory():
                if(newPage in self.getDisk().getMemory()):
                    self.removeFromDisk(newPage)
                self.allocateInRam(newPage, pid)
                self.addMemoryAccess(newPage)
            else:
                self.removeFromRam(self.getMarked())
                if(newPage in self.getDisk().getMemory()):
                    self.removeFromDisk(newPage)
                self.allocateInRam(newPage, pid)
                self.allocateInDisk(self.getMarked(), pid)
                self.addMemoryAccess(newPage)
        elif newPage not in self.getRam().getMemory():
            self.allocateInRam(newPage, pid)
            self.addMemoryAccess(newPage)
        if self.getMarked() in self.getState():
            data = self.getState()[self.getMarked()]
            data[7] = False
            self.addState(self.getMarked(), data)
        memoryAccesses = self.getMemoryAccesses()
        page2Remove = self.getRam().getMemory()[0]
        index = -1
        marked = [-1, index]
        for page2Remove in self.getRam().getMemory():
            if page2Remove != 0:
                index = memoryAccesses.index(page2Remove)
                if index > marked[1]:
                    marked = [page2Remove, index]
        self.setMarked(marked[0])
        data = self.getState()[marked[0]]
        data[7] = True
        self.addState(marked[0], data)
