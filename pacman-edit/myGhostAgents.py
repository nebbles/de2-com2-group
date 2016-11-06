# myGhostAgents.py

from game import Agent
from game import Actions
from game import Directions
import random
import numpy as np
import util

class MyGhostAgent( Agent ):
    def __init__( self, index ):
        self.index = index

    def getAction( self, state ):
        legalActions = state.getLegalActions( self.index )
        print "run getAction"

        # Find out if ghost is scared
        ghostState = state.getGhostState(self.index)
        isScared = ghostState.scaredTimer > 0

        # get self position and position of other ghost
        positionSelf = state.getGhostPosition(self.index)
        if self.index == 1: positionOther = state.getGhostPosition(2)
        if self.index == 2: positionOther = state.getGhostPosition(1)

        # get pacman position
        positionPacman = state.getPacmanPosition()

        # find 2 shortest paths
        path1,path2 = shortest_path(walls=state.getWalls(), start=positionSelf, end=positionPacman)

        # if ghosts are close together, second ghost takes path 2.
        ghostDistance = util.manhattanDistance(positionSelf, positionOther)
        if ghostDistance <= 4 and self.index == 2:
            myPath = path2  # take path2
        else:
            myPath = path1  # take path1

        myAction = getMyAction(myPath)
        return myAction
        #return legalActions[0] # currently returns first legal action available

    def getMyAction(self,path):
        legalActions = state.getLegalActions(self.index)
        # take path and extract first move direction
        currentPos = myPath[-1]
        nextPos = myPath[-2]

        north = [currentPos[0]+1,currentPos[1]]
        south = [currentPos[0]-1,currentPos[1]]
        east = [currentPos[0],currentPos[1]+1]
        west = [currentPos[0],currentPos[1]-1]

        if nextPos == north: return Directions.NORTH
        if nextPos == south: return Directions.SOUTH
        if nextPos == east: return Directions.EAST
        if nextPos == west: return Directions.WEST
        else:
            return legalActions[0]

    # SHORTEST PATH FUNCTION - returns shortest and second shortest path
    def shortest_path(walls, start, end):
        start = [start[0], start[1]]
        end = [end[0], end[1]]
        if start == end:
            return [start]

        neighbours = Queue()  # queue storing the next positions to explore
        neighbours.enqueue(start)
        counts = np.zeros_like((walls.width, walls.height), dtype=int)  # 2D array to store the distance from the start
        predecessors = np.zeros((counts.shape[0], counts.shape[1], 2), dtype=int)  # 2D array storing the predecessors
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
            print option
            print predecessors[end[0], end[1]]
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

        #print "counts:"
        #print counts

        return path1, path2

