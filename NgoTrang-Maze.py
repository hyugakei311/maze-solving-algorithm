# Trang Ngo (Katherine)
# Dr. Schep
# CIS 314 - 91
# 20 April 2017

#Using breadth first search revise the maze program from the recursion chapter
#to find the shortest path out of a maze

import turtle
from supp import *

PART_OF_PATH = 'O'
EXPLORED = '.'
OBSTACLE = '+'
TO_EXPLORE = '-'

class Maze:
    def __init__(self,mazeFileName):
        rowsInMaze = 0
        columnsInMaze = 0
        self.mazelist = []
        mazeFile = open(mazeFileName,'r')
        rowsInMaze = 0
        for line in mazeFile:
            rowList = []
            col = 0
            for ch in line[:-1]:
                rowList.append(ch)
                if ch == 'S':
                    self.startRow = rowsInMaze
                    self.startCol = col
                col = col + 1
            rowsInMaze = rowsInMaze + 1
            self.mazelist.append(rowList)
            columnsInMaze = len(rowList)

        self.rowsInMaze = rowsInMaze
        self.columnsInMaze = columnsInMaze
        self.xTranslate = -columnsInMaze/2
        self.yTranslate = rowsInMaze/2
        self.t = turtle.Turtle()
        self.t.shape('turtle')
        self.wn = turtle.Screen()
        self.wn.setworldcoordinates(-(columnsInMaze-1)/2-.5,-(rowsInMaze-1)/2-.5,(columnsInMaze-1)/2+.5,(rowsInMaze-1)/2+.5)

    def drawMaze(self):
        self.t.speed(10)
        self.wn.tracer(0)
        for y in range(self.rowsInMaze):
            for x in range(self.columnsInMaze):
                if self.mazelist[y][x] == OBSTACLE:
                    self.drawCenteredBox(x+self.xTranslate,-y+self.yTranslate,'orange')
        self.t.color('black')
        self.t.fillcolor('blue')
        self.wn.update()
        self.wn.tracer(1)

    def drawCenteredBox(self,x,y,color):
        self.t.up()
        self.t.goto(x-.5,y-.5)
        self.t.color(color)
        self.t.fillcolor(color)
        self.t.setheading(90)
        self.t.down()
        self.t.begin_fill()
        for i in range(4):
            self.t.forward(1)
            self.t.right(90)
        self.t.end_fill()

    def moveTurtle(self,x,y):
        self.t.up()
        self.t.setheading(self.t.towards(x+self.xTranslate,-y+self.yTranslate))
        self.t.goto(x+self.xTranslate,-y+self.yTranslate)

    def dropBreadcrumb(self,color):
        self.t.dot(10,color)

    def updatePosition(self,vertex,val=None):
        # move turtle using vertex instead of coordinates input
        if val:
            self.mazelist[vertex.getRow()][vertex.getCol()] = val
        self.moveTurtle(vertex.getCol(),vertex.getRow())

        if val == PART_OF_PATH:
            color = 'green' # color green the way out
        elif val == EXPLORED:
            color = 'black' # explored cells colored black
        elif val == TO_EXPLORE:
            color = 'gray' # cells to be explored colored gray
        else:
            color = None

        if color:
            self.dropBreadcrumb(color)

    def isExit(self,row,col):
        return (row == 0 or
                row == self.rowsInMaze-1 or
                col == 0 or
                col == self.columnsInMaze-1 )

    def __getitem__(self,idx):
        return self.mazelist[idx]


def searchFrom(maze, startRow, startColumn):
    # start with the current vertex at start cell
    # initiate a queue for vertices to be explored later
    start = Vertex(startRow,startColumn)
    start.setDistance(0)
    vertQueue = Queue()
    vertQueue.enqueue(start)
    currentVert = start

    # keep exploring vertices in queue unless queue is empty or currentVert is exit
    while (vertQueue.size() > 0) and not (maze.isExit(currentVert.getRow(),currentVert.getCol())):
        currentVert = vertQueue.dequeue()

        # if found exit, empty the queue and color the path out green
        if maze.isExit(currentVert.getRow(),currentVert.getCol()):
            vertQueue = Queue()
            maze.updatePosition(currentVert,PART_OF_PATH)
            while currentVert.getPred():
                currentVert = currentVert.getPred()
                maze.updatePosition(currentVert,PART_OF_PATH)
        
        else:
            # move turtle to the next vertex
            maze.updatePosition(currentVert,TO_EXPLORE)
            for nbr in nextMove(maze,currentVert.getRow(),currentVert.getCol()):
                nbr = Vertex(nbr[0],nbr[1]) # turn cell into vertex
                if (nbr.getStat() != TO_EXPLORE) and (nbr.getStat() != EXPLORED):
                    # if new cell, change status to TO_EXPLORE and color to gray
                    nbr.setStat(TO_EXPLORE)
                    maze.updatePosition(nbr,TO_EXPLORE)
                    # set distance and predecessor, then add to queue
                    nbr.setDistance(currentVert.getDistance() + 1)
                    nbr.setPred(currentVert)
                    vertQueue.enqueue(nbr)
            # change currentVert's status to EXPLORED and color to black
            currentVert.setStat(EXPLORED)
            maze.updatePosition(currentVert,EXPLORED)
    
# create a list of possible moves (right, down, left, up)
def nextMove(maze,x,y):
        newMoves = []
        moveOffsets = [(1,0),(0,-1),(-1,0),(0,1)]
        for i in moveOffsets:
            newX = x + i[0]
            newY = y + i[1]
            if legalCoord(maze,newX,newY):
                newMoves.append((newX,newY))
        return newMoves

# make sure the move is not out of the maze or already accounted for
def legalCoord(maze,x,y):
    if maze.mazelist[x][y] != OBSTACLE and maze.mazelist[x][y] != EXPLORED\
       and maze.mazelist[x][y] != TO_EXPLORE:
        return True
    else:
        return False

# Test:
myMaze = Maze('maze2.txt')
myMaze.drawMaze()
myMaze.updatePosition(Vertex(myMaze.startRow,myMaze.startCol))

searchFrom(myMaze, myMaze.startRow, myMaze.startCol)
