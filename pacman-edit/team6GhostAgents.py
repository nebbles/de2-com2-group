# team6GhostAgents.py

from game import Agent
from game import Actions
from game import Directions
from util import manhattanDistance
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
    if myPath == []: return legalActions[0]  # if path does not exist, then do the first legal action

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
    else:
        randomIndex = int(random.randint(0, len(legalActions) - 1))
        myAction = legalActions[randomIndex]
        return myAction  # else just pick random legal option (stops attempted backward movements)


def shortestPath(walls, start, end, returnOne=False):
    '''
    SHORTEST PATH FUNCTION - USING BFS ALGORITHM
    returns (path1, path2) if returnOne==False
    returns path1 if returnOne==True
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
    adjacent = [[end[0] + 1, end[1]], [end[0] - 1, end[1]], [end[0], end[1] + 1], [end[0], end[1] - 1]]
    minoption = None
    for option in adjacent:
        if option != predecessors[end[0], end[1]].tolist() and not walls[option[0]][option[1]]:
            if minoption == None: minoption = option  # for first iteration
            if counts[minoption[0], minoption[1]] >= counts[option[0], option[1]]:
                minoption = option  # update min option with a better min

    # construct path 1
    while n != start:
        if n == start:
            break
        path1.append(n)
        n = predecessors[n[0], n[1]].tolist()
    path1.append(start)

    if returnOne == True: # if only shortest path is needed from function then skip the construction of path2
        return path1

    # we must exit function now if an alternate route could not be found, this is because minoption is None.
    if minoption == None:
        path2 = path1
        return path1, path2

    # construct path 2
    n = minoption
    loopcount = 0
    while n != start:
        if loopcount > 50:
            return path1, path1
        if n == start:
            break
        path2.append(n)
        n = predecessors[n[0], n[1]].tolist()
        loopcount += 1
    path2.append(start)
    path2.insert(0, end)

    # print 'counts \n', counts  # debug
    # print 'predecessors \n', predecessors  # debug
    return path1, path2


def similarPath(pathA, pathB, steps):
    while len(pathA) < steps + 1 or len(pathB) < steps + 1:
        steps -= 1
        if steps == 0:
            return False

    duplicate = []
    for i in range(0, steps):
        if pathA[i] == pathB[i]:
            duplicate.append(True)
        else:
            duplicate.append(False)
    if sum(duplicate) == steps:  # if all the steps are True
        return True  # paths are similar
    else:
        return False  # paths are not similar


class team6GhostAgents(Agent):
    def __init__(self, index):
        self.index = index

    def getAction(self, state):
        legalActions = state.getLegalActions(self.index)
        numberOfGhosts = len(state.data.agentStates) -1  # state.data.agentStates[agentIndex]

        scared = state.getGhostState(self.index).scaredTimer > 0
        shouldRun = False
        if scared: shouldRun = True

        # Get self position
        posX,posY = state.getGhostPosition(self.index)
        positionSelf = (int(posX), int(posY))

        if numberOfGhosts > 1:
            # Get position of other ghost (ghost 2 [or greater] just looks to ghost 1)
            if self.index == 1:
                posX, posY = state.getGhostPosition(2)
                positionOther = (int(posX), int(posY))
            else:
                posX, posY = state.getGhostPosition(1)
                positionOther = (int(posX), int(posY))

        # Get pacman position
        posX, posY = state.getPacmanPosition()
        positionPacman = (int(posX), int(posY))

        # Get the walls
        walls = state.getWalls()  # get walls of map

        # Get remaining capsules and find if the pacman closest distance to capsule is within a certain value
        capsules = state.getCapsules()
        pathLengths = []
        for caps in capsules:
            path1 = shortestPath(walls=walls, start=caps, end=positionPacman, returnOne=True)
            pathLengths.append(len(path1))
        for length in pathLengths:
            if length < 3:  # distance that ghost starts to back away from pacman
                shouldRun = True

        if shouldRun:
            speed = 0.5
            actionVectors = [Actions.directionToVector(a, speed) for a in legalActions]
            newPositions = [(positionSelf[0] + a[0], positionSelf[1] + a[1]) for a in actionVectors]
            distancesToPacman = [manhattanDistance(positionSelf, positionPacman) for positionSelf in newPositions]
            bestScore = max(distancesToPacman)
            bestActions = [action for action, distance in zip(legalActions, distancesToPacman) if
                           distance == bestScore]
            randomIndex = int(random.randint(0, len(bestActions) - 1))
            myAction = bestActions[randomIndex]
        else:
            path1, path2 = shortestPath(walls=walls, start=positionSelf, end=positionPacman)  # find 2 shortest paths for self
            myPath = path1  # set path of self to shortest path

            if numberOfGhosts > 1:
                pathOther, other = shortestPath(walls=walls, start=positionOther, end=positionPacman)  # find 2 shortest paths of other ghost of two
                stepsCompared = 3
                similar = False  # set paths are similar flag to False
                similar = similarPath(pathOther, path1, stepsCompared)

                if similar:  # if paths of ghost 1 and 2 are similar
                    if len(path1) > len(pathOther):  # if self path is longer than ghost teammate then
                        myPath = path2  # take path2
                    if len(path1) < len(pathOther):  # if self path is shorter than ghost teammate then
                        myPath = path1  # take path1 - shortest path
                    if len(path1) == len(pathOther):  # if path length is the same then
                        if self.index == 2: myPath = path2  # ghost 2 takes its second best route

                if len(path2) > 20:  # if path length is greater than 20
                    myPath = path1

            myAction = getPathAction(self, state, myPath)

        return myAction