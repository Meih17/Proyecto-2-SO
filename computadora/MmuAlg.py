from algoritmos.Random import Random
from algoritmos.SecondChance import SecondChance
import time

class MmuAlg:

    def __init__(self, algorithm):
        self.setCurrentId(1)
        self.setTable({})
        self.setAlgorithm(algorithm)
        self.setFragDic({})
    
    # GETTERS
    def getCurrentId(self):
        return self.__id

    def getTable(self):
        return self.__memory
    
    def getAlgorithm(self):
        return self.__algorithm  

    def getFragDic(self):
        return self.__fragDic 


    # SETTERS
    def setCurrentId(self, id):
        self.__id = id

    def setTable(self, memory):
        self.__memory = memory

    def setAlgorithm(self, algorithm):
        self.__algorithm = algorithm

    def setFragDic(self, fragDic):
        self.__fragDic = fragDic


    # FUNCTIONS
    def getState(self):
        return self.getAlgorithm().getState()

    def incrementId(self):
        tempId = self.getCurrentId()
        tempId += 1
        self.setCurrentId(tempId)
        return self.getCurrentId() - 1

    def addInTable(self, key, value):
        tempDic = self.getTable()
        tempDic[key] = value
        self.setTable(tempDic)

    def removeFromTable(self, key):
        tempDic = self.getTable()
        del tempDic[key]
        self.setTable(tempDic)

    def updateFragDic(self, key, value):
        tempDic = self.getFragDic()
        tempDic[key] = value
        self.setFragDic(tempDic)

    def killProcess(self, pointerList):
        for pointer in pointerList:
            for page in self.getTable()[pointer]:
                self.updateFragDic(page, 0)
                if page in self.getAlgorithm().getRam().getMemory():
                    self.getAlgorithm().getRam().removePage(page)
                    self.getAlgorithm().delPag(page)
                if page in self.getAlgorithm().getDisk().getMemory():
                    self.getAlgorithm().getDisk().removePage(page)
                self.getAlgorithm().rmvState(page)
            self.removeFromTable(pointer)
        self.getAlgorithm().addExecTime(10)

    def finish(self):
        tempRam = self.getAlgorithm().getRam().getMemory()
        tempTable = self.getTable()
        for page in tempRam:
            page = 0
        self.getAlgorithm().getRam().setMemory(tempRam)
        self.getAlgorithm().getDisk().setMemory([])
        self.setTable(tempTable)
    
    def markePage(self, key, isMark):
        tempDic = self.getAlgorithm().getState()
        if key in tempDic:
            list = tempDic[key]
            if(isMark == 1):
                list[7] = True
            else:
                list[7] = False  
            tempDic[key] = list
            self.getAlgorithm().setState(tempDic)

    def getPages(self, ptr, bytesSize):
        if ptr not in self.getTable():
            pagesList  = []
            kbSize = bytesSize/1024
            pag = self.incrementId()
            pagesList.append(pag)
            kbSize -= 4
            while(kbSize > 4):
                pag = self.incrementId()
                pagesList.append(pag)
                kbSize -= 4
            frag = abs(kbSize)
            if frag != 0:
                self.updateFragDic(pag, frag)
            self.addInTable(ptr, pagesList)
            return pagesList
        else:
            return self.getTable()[ptr]

    def getTotalFrag(self):
        totalFrag = 0
        tempDic = self.getFragDic()
        for key in tempDic:
            totalFrag += tempDic[key]
        return totalFrag
    
    def execute(self, ptr, bytesSize, pid):
        # data [PageID, PTR, LOADED, L-ADDR, M-ADDR, LOADED-T, MARK]
        algoritmo = self.getAlgorithm()
        pagesList  = self.getPages(ptr, bytesSize)
        for page in pagesList:
            time.sleep(0.0000000001)
            if page in algoritmo.getRam().getMemory():
                algoritmo.allocate(page, pid)
            elif algoritmo.getRam().isFull() and page not in algoritmo.getRam().getMemory():
                if 0 in algoritmo.getRam().getMemory():
                    algoritmo.allocate(page, pid)
                else:
                    algoritmo.allocate(page, pid)
            else:
                algoritmo.allocate(page, pid)
                    
            

      

    

