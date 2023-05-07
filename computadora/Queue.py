class Queue:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def queue(self, item):
        self.items.insert(0,item)

    def pop(self):
        return self.items.pop()

    def len(self):
        return len(self.items)

    def clear(self):
        self.items = []
    
    def setQueue(self, items):
        self.items = items
    
    def isIn(self, e):
        return e in self.items

    def getQueue(self):
        return list(reversed(self.items))