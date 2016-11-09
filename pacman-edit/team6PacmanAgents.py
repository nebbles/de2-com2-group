# myPacmanAgents.py

from team6GhostAgents import *
from pacman import Directions
from game import Agent
from game import GameStateData
import random
import game
import util


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