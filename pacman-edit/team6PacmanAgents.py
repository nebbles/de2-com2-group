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


class team6PacmanAgents(game.Agent):

    def pacmanDanger(self, state, pacmanPos, ghostPosns):
        danger = 'ok'
        critDangerDist = 3  # minimum is 3, recommended 3 or 4
        walls = state.getWalls()

        # check path distance of ghosts from pacman
        distances = []
        for ghost in ghostPosns:
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
            ghostPosition = state.getGhostPosition(ghostIndex)
            if ghostState.scaredTimer > 0:
                positionScaredGhosts.append(ghostPosition)
            else:
                positionAngryGhosts.append(ghostPosition)




        # ghost1State = state.getGhostState(1)
        # ghost2State = state.getGhostState(2)
        # ghost1IsScared = ghost1State.scaredTimer > 0
        # ghost2IsScared = ghost2State.scaredTimer > 0
        # positionGhosts = state.getGhostPositions()
        #
        # scaredGhostsPosns = []
        # chaseGhostsPositions = []
        # if ghost1IsScared:
        #     scaredGhostsPosns.append(positionGhosts[0])
        # if ghost2IsScared:
        #     scaredGhostsPosns.append(positionGhosts[1])
        #
        # for chaseGhost in positionGhosts:
        #
        #     if chaseGhost
        #         chaseGhostsPositions.append()

        # Load pacman information
        positionPacman = state.getPacmanPosition()

        # find the pacman danger
        danger = self.pacmanDanger(state, pacmanPos=positionPacman, ghostPosns=positionAngryGhosts)

        # act based on danger

        if danger == 'critical':
            pass  # act on critical danger
        if danger == 'ok':
            if len(positionScaredGhosts) > 0:
                # find nearest scared ghost
                distanceScaredGhosts = []
                for positionScaredGhost in positionScaredGhosts:
                    distance = shortestPath(walls=walls, start=positionPacman, end=positionScaredGhost)
                    distanceScaredGhosts.append(distance)
                index = distanceScaredGhosts.index(min(distanceScaredGhosts))
                positionClosestScaredGhost = positionScaredGhosts[index]

                # amend walls data with ghost positions
                wallList = getUpdatedWalls(state, ghostPositions=positionAngryGhosts)

                # shortest path to nearest scared ghost
                path1, path2 = shortestPath(walls=wallList, start=positionPacman, end=positionClosestScaredGhost)
                myAction = getPathAction(self, state, path1)  # getPathAction and assign to myAction

            else:
                # find nearest capsule
                positionCapsules = state.getCapsules()
                distanceCapsules = []
                for capsule in capsules:
                    distance = shortestPath(walls=walls, start=positionPacman, end=capsule)
                    distanceCapsules.append(distance)
                index = distanceCapsules.index(min(distanceCapsules))
                positionClosestCapsule = positionCapsules[index]

                # amend walls data with ghost positions
                wallList = getUpdatedWalls(state, ghostPositions=positionAngryGhosts)

                # shortest path to nearest capsule
                path1, path2 = shortestPath(walls=wallList, start=positionPacman, end=positionClosestCapsule)
                myAction = getPathAction(self, state, path1)  # getPathAction and assign to myAction

        return myAction
        #return Directions.STOP

