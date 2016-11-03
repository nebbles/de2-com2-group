# myPacmanAgents.py

from pacman import Directions
from game import Agent
import random
import game
import util

class MyPacmanAgent(game.Agent):

    def pacmanDanger(pacmanPos,ghostPos):
        danger = 'ok'

        # check manhattanDistance of ghost from pacman
        # if ghost is in danger return danger
        # if ghost in crit zone flag critical

        return danger

    def priority(pacmanPos,ghostPos,isScared):
        if isScared: # check ghost
            return 'chase' # return chase priority

        pacmanDanger(pacmanPos=pacmanPos,ghostPos=ghostPos) # check danger
        # check energisers
        # check biscuits

        # return a plan for the pacman based on danger and other info

    def getAction(self, state):

        # Load ghost information
        ghostState = state.getGhostState( 1 )
        ghostPosition = state.getGhostPosition( 1 )
        ghostIsScared = ghostState.scaredTimer > 0

        # Load pacman information
        pacmanPosition = state.getPacmanPosition()

        # Decide what plan the pacman will take
        plan = priority(pacmanPos=pacmanPosition,ghostPos=ghostPosition,isScared=ghostIsScared)

        # choose target tile based on priority plan

        return Directions.STOP

'''
    "A ghost that prefers to rush Pacman, or flee when scared."
    def __init__( self, index, prob_attack=0.8, prob_scaredFlee=0.8 ):
        self.index = index
        self.prob_attack = prob_attack
        self.prob_scaredFlee = prob_scaredFlee

    def getDistribution( self, state ):
        # Read variables from state
        ghostState = state.getGhostState( self.index )
        legalActions = state.getLegalActions( self.index )
        pos = state.getGhostPosition( self.index )
        isScared = ghostState.scaredTimer > 0

        speed = 1
        if isScared: speed = 0.5

        actionVectors = [Actions.directionToVector( a, speed ) for a in legalActions]
        newPositions = [( pos[0]+a[0], pos[1]+a[1] ) for a in actionVectors]
        pacmanPosition = state.getPacmanPosition()

        # Select best actions given the state
        distancesToPacman = [manhattanDistance( pos, pacmanPosition ) for pos in newPositions]
        if isScared:
            bestScore = max( distancesToPacman )
            bestProb = self.prob_scaredFlee
        else:
            bestScore = min( distancesToPacman )
            bestProb = self.prob_attack
        bestActions = [action for action, distance in zip( legalActions, distancesToPacman ) if distance == bestScore]

        # Construct distribution
        dist = util.Counter()
        for a in bestActions: dist[a] = bestProb / len(bestActions)
        for a in legalActions: dist[a] += ( 1-bestProb ) / len(legalActions)
        dist.normalize()
        return dist
