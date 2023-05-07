class Disk:

    def __init__(self):
        self.setUsedMemory(0)
        self.setMemory([])
    
    # GETTERS
    def getMemory(self):
        return self.__memory

    def getUsedMemory(self):
        return self.__usedMemory


    # SETTERS
    def setMemory(self, memory):
        self.__memory = memory

    def setUsedMemory(self, usedMemory):
        self.__usedMemory = usedMemory


    # FUNCTIONS
    def getAddr(self, page):
        return self.getMemory().index(page)

    def allocatePage(self, page):
        tempMem = self.getMemory()
        tempMem.append(page)
        tempUsedMemory = self.getUsedMemory()
        tempUsedMemory += 4
        self.setUsedMemory(tempUsedMemory)
        self.setMemory(tempMem)
    
    def removePage(self, page):
        tempMem = self.getMemory()
        tempUsedMemory = self.getUsedMemory()
        tempUsedMemory -= 4
        index = tempMem.index(page)
        tempMem.remove(page)
        tempMem.insert(index, 0)
        self.setUsedMemory(tempUsedMemory)
        self.setMemory(tempMem)