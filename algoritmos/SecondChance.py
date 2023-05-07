from computadora.Ram import Ram
from computadora.Disk import Disk

class SecondChance:

    def __init__(self):
        self.setRam(Ram())
        self.setDisk(Disk())
        self.setClock({})
        self.setVictim(0)
        self.setExecTime(0)
        self.setState({})
        self.setThrashingTime(0)
    
    # GETTERS
    def getRam(self):
        return self.__ram

    def getDisk(self):
        return self.__disk

    def getClock(self):
        return self.__clock

    def getVictim(self):
        return self.__victim

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

    def setClock(self, clock):
        self.__clock = clock

    def setVictim(self, victim):
        self.__victim = victim

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

    def updateClock(self, key, value, pid):
        tempClock = self.getClock()
        tempClock[key] = value
        self.setClock(tempClock)

    def addExecTime(self, time):
        tempExecTime = self.getExecTime()
        tempExecTime += time
        self.setExecTime(tempExecTime)

    def addThrashingTime(self, time):
        tempTime = self.getThrashingTime()
        tempTime += time
        self.setThrashingTime(tempTime)


    def allocate(self, newPage, pid):
        if self.getRam().isFull():
            if newPage not in self.getRam().getMemory():
                if 0 in self.getRam().getMemory():
                    if(newPage in self.getDisk().getMemory()):
                        self.removeFromDisk(newPage)
                    self.allocateInRam(newPage, pid)
                    self.updateClock(newPage, 1, pid)
                else:
                    tempRam = self.getRam().getMemory()
                    victim = self.getVictim()
                    replaced = False
                    index = victim
                    while not replaced:
                        if self.getClock()[tempRam[index]] == 0:
                            page2Remove = tempRam[index]
                            self.updateClock(newPage, 1, pid)
                            replaced = True
                        else:
                            self.updateClock(tempRam[index], 0, pid)
                        index += 1
                        if(index == len(tempRam)):
                            index = 0
                    self.setVictim(index)
                    self.removeFromRam(page2Remove)
                    if(newPage in self.getDisk().getMemory()):
                        self.removeFromDisk(newPage)
                    self.allocateInRam(newPage, pid)
                    self.allocateInDisk(page2Remove, pid)
            else:
                self.updateClock(newPage, 1, pid)
        elif newPage not in self.getRam().getMemory():
            self.allocateInRam(newPage, pid)
            self.updateClock(newPage, 1, pid)
        for key in self.getClock():
            if key in self.getState():
                tempState = self.getState()[key]
                if self.getClock()[key] == 1:
                    tempState[7] = True
                else:
                    tempState[7] = False
                self.addState(key, tempState)