# class Vertex:
class Vertex:
    def __init__(self,row,col):
        self.id = (row,col)
        self.connectedTo = {}
        self.distance = None
        self.predecessor = None
        self.status = None # EXPLORE or TO_EXPLORE

    def addNeighbor(self,nbr,weight=0):
        self.connectedTo[nbr] = weight

    def __str__(self):
        return str(self.id) + ' connectedTo: ' + str([x.id for x in self.connectedTo])

    def getConnections(self):
        return self.connectedTo.keys()

    def getId(self):
        return self.id

    def getWeight(self,nbr):
        return self.connectedTo[nbr]

    def getDistance(self):
        return self.distance

    def setDistance(self,dist):
        self.distance = dist

    def getPred(self):
        return self.predecessor

    def setPred(self,vert):
        self.predecessor = vert

    def getStat(self):
        return self.status

    def setStat(self,status):
        self.status = status

    def getRow(self):
        return self.id[0]

    def getCol(self):
        return self.id[1]

#class Queue
class Queue:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def enqueue(self, item):
        self.items.insert(0,item)

    def dequeue(self):
        return self.items.pop()

    def size(self):
        return len(self.items)
