# myGhostAgents.py

from game import Agent
from game import Actions
from game import Directions
import random
import numpy as np
import util


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


def getPathAction(self, state, myPath): # take path and extract first move direction

    legalActions = state.getLegalActions(self.index)  # get legal actions of self
    currentPos = myPath[-1]  # current position is last item in list
    nextPos = myPath[-2]  # position after current is penultimate item in list

    east = [currentPos[0] + 1, currentPos[1]]
    west = [currentPos[0] - 1, currentPos[1]]
    north = [currentPos[0], currentPos[1] + 1]
    south = [currentPos[0], currentPos[1] - 1]

    # if next suggested position is 'direction' and 'direction' is a legal action then move 'direction'
    if nextPos == north and Directions.NORTH in legalActions: return Directions.NORTH
    if nextPos == south and Directions.SOUTH in legalActions: return Directions.SOUTH
    if nextPos == east and Directions.EAST in legalActions: return Directions.EAST
    if nextPos == west and Directions.WEST in legalActions: return Directions.WEST
    else: return legalActions[0]  # else just fo the first legal option (stops attempted backward movements)


def shortestPath(walls, start, end):
    '''
    SHORTEST PATH FUNCTION
    returns path1,path2
    path1 is shortest path and path2 is second shortest path
    '''
    start = [start[0], start[1]]
    end = [end[0], end[1]]
    if start == end:
        return [start]

    neighbours = Queue()  # queue storing the next positions to explore
    neighbours.enqueue(start)
    counts = np.zeros((walls.width, walls.height),
                      dtype=int)  # 2D array to store the distance from the start to all visted points
    predecessors = np.zeros((counts.shape[0], counts.shape[1], 2),
                            dtype=int)  # 2D array storing the predecessors (past points allowing path to be retraced)
    counts[start[0], start[1]] = 1

    # loop until the end position is found
    while not neighbours.isEmpty():
        n = neighbours.dequeue()
        # add all the valid neighbours to the list and remember from where they came from
        if n != end:
            for neighbour in [[n[0] - 1, n[1]], [n[0] + 1, n[1]], [n[0], n[1] - 1],
                              [n[0], n[1] + 1]]:  # for all neighbors to current
                if not walls[neighbour[0]][neighbour[1]] and counts[neighbour[0], neighbour[1]] == 0:
                    neighbours.enqueue(neighbour)
                    predecessors[neighbour[0], neighbour[1]] = n
                    counts[neighbour[0], neighbour[1]] = counts[n[0], n[1]] + 1

    if counts[end[0], end[1]] == 0:
        return []  # path not found
    path1 = []
    path2 = []
    n = end

    # calculate alternate route start point for reconstruction
    n = end
    adjacent = [[end[0] + 1, end[1]], [end[0] - 1, end[1]], [end[0], end[1] + 1], [end[0], end[1] - 1]]

    minoption = None

    for option in adjacent:
        # print option
        # print predecessors[end[0], end[1]]
        if option != predecessors[end[0], end[1]].tolist() and not walls[option[0]][option[1]]:
            if minoption == None:
                minoption = option
            if counts[minoption[0], minoption[1]] >= counts[option[0], option[1]]:
                minoption = option

    # construct path 1
    while n != start:
        if n == start:
            break
        path1.append(n)
        n = predecessors[n[0], n[1]].tolist()
    path1.append(start)

    # construct path 2
    n = minoption
    while n != start:
        if n == start:
            break
        path2.append(n)
        n = predecessors[n[0], n[1]].tolist()
    path2.append(start)
    path2.insert(0, end)

    # print "counts:"
    # print counts
    # print predecessors

    return path1, path2

class MyGhostAgent( Agent ):
    def __init__( self, index ):
        self.index = index

    def getAction(self, state):
        legalActions = state.getLegalActions(self.index)

        # Find out if ghost is scared
        ghostState = state.getGhostState(self.index)
        isScared = ghostState.scaredTimer > 0

        # get self position and position of other ghost
        posX,posY = state.getGhostPosition(self.index)
        positionSelf = (int(posX),int(posY))
        #print 'position of self',positionSelf
        if self.index == 1: positionOther = state.getGhostPosition(2)
        if self.index == 2: positionOther = state.getGhostPosition(1)

        # get pac-man position
        positionPacman = state.getPacmanPosition()

        #self.WallGrid = []
        #self.WallArray = []
        '''
        self.WallsGrid = state.getWalls()
        self.WallArray = np.zeros((self.WallsGrid.width, self.WallsGrid.height), dtype=bool)

        for y in range(0, self.WallsGrid.height):
            for x in range(0, self.WallsGrid.width):
                if self.WallsGrid[x][y] == True:
                    self.WallArray[x][y] = True

        print self.WallArray
        '''
        # find 2 shortest paths

        self.walls = state.getWalls()
        path1, path2 = shortestPath(walls=self.walls,start=positionSelf, end=positionPacman)

        #print path2
        # if ghosts are close together, second ghost takes path 2.
        ghostSeperation = util.manhattanDistance(positionSelf, positionOther)
        if ghostSeperation <= 4 and self.index == 2:
            myPath = path2  # take path2
        else:
            myPath = path1  # take path1

        #myPath = path1

        myAction = getPathAction(self, state, myPath)
        return myAction
        # return legalActions[0] # currently returns first legal action available



