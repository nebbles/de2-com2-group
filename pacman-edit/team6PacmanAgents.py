# team6PacmanAgents.py

from pacman import Directions
from game import Agent
from game import Actions
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
    else: return legalActions[0]  # else just fo the first legal option (stops attempted backward movements)


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


def getUpdatedWalls(state, ghostPositions):
    walls = state.getWalls()
    if ghostPositions == []:  # if there are no ghost positions to amend to walls data
        return walls  # return normal wall data

    import copy
    wallList = copy.deepcopy(walls)  # take a copy of the wall data

    for ghost in ghostPositions:  # for all ghost coordinates passed into function
        x, y = ghost
        wallList[x][y] = True  # modify walls data to place a wall where the ghost is
    return wallList  # return modified wall data


def getFoodList(state):  # get food coordinates as a list
    foods = state.getFood()
    positionFoods = foods.asList()
    return positionFoods


def getNearestItem(walls, positionSelf, positionItems):
    distanceItems = []
    for item in positionItems:  # list of coordinates for specified item
        path1 = shortestPath(walls=walls, start=item, end=positionSelf, returnOne=True)
        distance = len(path1)  # take the length of the shortest path from self to item
        if distance > 0:
            distanceItems.append(distance)  # produce a list of distances of self from items

    if distanceItems == []:
        return None

    index = distanceItems.index(min(distanceItems))  # find the index of the item with minimum distance to self
    positionClosestItem = positionItems[index]
    print distanceItems
    return positionClosestItem  # return coordinates of closest item


class team6PacmanAgents(game.Agent):

    def pacmanDanger(self, state, pacmanPos, ghostPosns):
        danger = 'ok'  # set danger flag to 'ok' by default
        critDangerDist = 3  # critical state only when ghost is right next to pacman (one space gap)
        walls = state.getWalls()

        # check path distance of ghosts from pacman
        distances = []
        for ghost in ghostPosns:
            path1 = shortestPath(walls=walls, start=ghost, end=pacmanPos, returnOne=True)
            dist = len(path1)
            distances.append(dist)

        # if not all distances are greater than the critical zone then the pacman is in critical danger
        if not all(i > critDangerDist for i in distances):
            danger = 'critical'  # if ghost in critical zone, flag critical
        return danger

    def getAction(self, state):
        legalActions = state.getLegalActions()
        myAction = legalActions[0]  # set default behaviour in case myAction is not assigned

        # Load ghost information
        numberOfGhosts = len(state.data.agentStates) -1  # state.data.agentStates[agentIndex]
        positionScaredGhosts = []
        positionAngryGhosts = []

        for ghostIndex in range(1, numberOfGhosts + 1):
            ghostState = state.getGhostState(ghostIndex)
            posX, posY = state.getGhostPosition(ghostIndex)
            ghostPosition = (int(posX), int(posY))
            if ghostState.scaredTimer > 2:  # if ghost is about to change back, do not chase it
                positionScaredGhosts.append(ghostPosition)
            else:
                positionAngryGhosts.append(ghostPosition)

        # Load pacman information
        posX, posY = state.getPacmanPosition()
        positionPacman = (int(posX), int(posY))

        # Set the danger flag for the pacman
        danger = self.pacmanDanger(state, pacmanPos=positionPacman, ghostPosns=positionAngryGhosts)

        # Act based on danger flag
        walls = state.getWalls()  # variable for unchanged version of walls data
        newWalls = getUpdatedWalls(state, ghostPositions=positionAngryGhosts)  # amend walls data with ghost pos.s

        if danger == 'critical':  # act on critical danger
            speed = 1
            actionVectors = [Actions.directionToVector(a, speed) for a in legalActions]
            newPositions = [(positionPacman[0]+a[0], positionPacman[1]+a[1]) for a in actionVectors]
            positionClosestAngryGhost = getNearestItem(walls, positionPacman, positionAngryGhosts)

            # Select best actions given the state
            distancesToAngryGhost = [util.manhattanDistance(positionPacman, positionClosestAngryGhost) for positionPacman in newPositions]
            bestScore = max(distancesToAngryGhost)
            bestActions = [action for action, distance in zip(legalActions, distancesToAngryGhost) if distance == bestScore]

            randomIndex = int(random.randint(0, len(bestActions)-1))
            myAction = bestActions[randomIndex]

        if danger == 'ok':
            if len(positionScaredGhosts) > 0:
                positionClosestScaredGhost = getNearestItem(newWalls, positionPacman, positionScaredGhosts) # find nearest scared ghost
                if not positionClosestScaredGhost == None:
                    path1 = shortestPath(walls=newWalls, start=positionPacman, end=positionClosestScaredGhost, returnOne=True)
                    myAction = getPathAction(self, state, path1)  # getPathAction and assign to myAction
                    return myAction

            positionCapsules = state.getCapsules()
            if len(positionCapsules) > 0:
                positionClosestCapsule = getNearestItem(newWalls, positionPacman, positionCapsules)  # find nearest capsule
                if not positionClosestCapsule == None:
                    path1 = shortestPath(walls=newWalls, start=positionPacman, end=positionClosestCapsule, returnOne=True)
                    myAction = getPathAction(self, state, path1)  # getPathAction and assign to myAction
                    return myAction

            # No capsules and no ghosts to chase, so eat food
            positionFoods = getFoodList(state)
            positionClosestFood = getNearestItem(newWalls, positionPacman, positionFoods)  # find nearest food
            if not positionClosestFood == None:
                path1 = shortestPath(walls=newWalls, start=positionPacman, end=positionClosestFood, returnOne=True)
                myAction = getPathAction(self, state, path1)  # getPathAction and assign to myAction
                return myAction

        return myAction