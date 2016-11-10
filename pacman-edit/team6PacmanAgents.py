# myPacmanAgents.py

from pacman import Directions
from game import Agent
from game import GameStateData
import random
import game
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

    # construct path 2
    n = minoption
    while n != start:
        if n == start:
            break
        path2.append(n)
        n = predecessors[n[0], n[1]].tolist()
    path2.append(start)
    path2.insert(0, end)

    # print 'counts \n', counts  # debug
    # print 'predecessors \n', predecessors  # debug

    return path1, path2


def wallsConverted(state):
    walls = state.getWalls()
    wallList = []
    for x in walls:
        for y in walls[x]:
            wallList[x][y] = walls[x][y]
    return wallList


def getUpdatedWalls(state, ghostPositions):
    wallList = wallsConverted(state)
    for ghost in positionGhosts:
        x, y = ghost
        wallList[x][y] = True
    return wallList


def getFoodList(state):
    getFoods = state.getFood()
    positionFood = []
    for x in getFoods:
        for y in getFoods[x]:
            if getFoods[x][y]:
                positionFood.append((x, y))
    return positionFood


def getNearestItem(positionSelf, positionItems):
    distanceItems = []
    for item in positionItems:
        distance = shortestPath(walls=walls, start=positionSelf, end=item)
        distanceItems.append(distance)
    index = distanceItems.index(min(distanceItems))
    positionClosestItem = positionItems[index]
    return positionClosestItem


def getActionOfShortestPath(walls, start, end):
    path1, path2 = shortestPath(walls=walls, start=start, end=end)
    myAction = getPathAction(self, state, path1)  # getPathAction and assign to myAction
    return myAction


class team6PacmanAgents(game.Agent):

    def pacmanDanger(self, state, pacmanPos, ghostPosns):
        danger = 'ok'
        critDangerDist = 3  # minimum is 3, recommended 3 or 4
        walls = state.getWalls()

        # check path distance of ghosts from pacman
        distances = []
        for ghost in ghostPosns:
            print walls
            print pacmanPos
            print ghost
            dist, other = shortestPath(walls=walls, start=pacmanPos, end=ghost)
            distances.append(dist)

        if not all(i > critDangerDist for i in distances):
            danger = 'critical'  # if ghost in critical zone, flag critical
        return danger

    def getAction(self, state):

        # Load ghost information
        numberOfGhosts = len(state.data.agentStates) -1  # state.data.agentStates[agentIndex]
        positionScaredGhosts = []
        positionAngryGhosts = []

        for ghostIndex in range(1, numberOfGhosts + 1):
            ghostState = state.getGhostState(ghostIndex)
            posX, posY = state.getGhostPosition(ghostIndex)
            ghostPosition = (int(posX), int(posY))
            if ghostState.scaredTimer > 0:
                positionScaredGhosts.append(ghostPosition)
            else:
                positionAngryGhosts.append(ghostPosition)

        # Load pacman information
        posX, posY = state.getPacmanPosition()
        positionPacman = (int(posX), int(posY))

        # find the pacman danger
        danger = self.pacmanDanger(state, pacmanPos=positionPacman, ghostPosns=positionAngryGhosts)

        # act based on danger
        wallList = getUpdatedWalls(state, ghostPositions=positionAngryGhosts)  # amend walls data with ghost pos.s
        if danger == 'critical':
            pass  # act on critical danger
        if danger == 'ok':
            if len(positionScaredGhosts) > 0:
                positionClosestScaredGhost = getNearestItem(positionPacman, positionScaredGhosts) # find nearest scared ghost
                # action of shortest path to nearest scared ghost
                myAction = getActionOfShortestPath(walls=wallList, start=positionPacman, end=positionClosestScaredGhost)
                return myAction

            positionCapsules = state.getCapsules()
            if len(positionCapsules) > 0:
                positionClosestCapsule = getNearestItem(positionPacman, positionCapsules)  # find nearest capsule
                # action of shortest path to nearest capsule
                myAction = getActionOfShortestPath(walls=wallList, start=positionPacman, end=positionClosestCapsule)
                return myAction

            # No capsules and no ghosts to chase, so eat
            positionFoods = getFoodList(state)
            positionClosestFood = getNearestItem(positionPacman, positionFoods)  # find nearest food
            # shortest path to nearest capsule
            myAction = getActionOfShortestPath(walls=wallList, start=positionPacman, end=positionClosestFood)
            return myAction

        return myAction
        #return Directions.STOP