from algoritmos.Optimal import Optimal
from computadora.Queue import Queue

class MmuOpt:
    def __init__(self, memCalls, pointersDic, process):
        self.setPointersDic(pointersDic)
        self.setTable({})
        self.setCurrentId(1)
        self.setFragDic({})
        self.setAlgorithm(Optimal(self.getPageCalls(memCalls)))
        self.setProcess(process)
    
    # GETTERS
    def getCurrentId(self):
        return self.__id

    def getTable(self):
        return self.__memory
    
    def getProcess(self):
        return self.__process

    def getAlgorithm(self):
        return self.__algorithm  

    def getPointersDic(self):
        return self.__pointersDic 

    def getFragDic(self):
        return self.__fragDic   


    # SETTERS
    def setCurrentId(self, id):
        self.__id = id

    def setTable(self, memory):
        self.__memory = memory

    def setAlgorithm(self, algorithm):
        self.__algorithm = algorithm

    def setPointersDic(self, pointersDic):
        self.__pointersDic = pointersDic

    def setProcess(self, process):
        self.__process = process

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
                if page in self.getAlgorithm().getRam().getMemory():
                    self.getAlgorithm().getRam().removePage(page)
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

    def getPages(self, ptr, bytesSize):
        # data [PageID, PTR, LOADED, L-ADDR, M-ADDR, LOADED-T, MARK]
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

    def getPageCalls(self, memCalls):
        pageCalls = Queue()
        queue = memCalls
        while(not queue.isEmpty()):
            pointer  = queue.pop()
            pageCalls.queue(self.getPages(pointer, self.getPointersDic()[pointer]))
        return pageCalls

    def getTotalFrag(self):
        totalFrag = 0
        tempDic = self.getFragDic()
        for key in tempDic:
            if key in self.getAlgorithm().getRam().getMemory():
                totalFrag += tempDic[key]
        return totalFrag

    def execute(self, pid):
        self.getAlgorithm().allocateNext(pid)