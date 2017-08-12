# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for 
# educational purposes provided that (1) you do not distribute or publish 
# solutions, (2) you retain this notice, and (3) you provide clear 
# attribution to UC Berkeley, including a link to 
# http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero 
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and 
# Pieter Abbeel (pabbeel@cs.berkeley.edu).
import sys

from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
#        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        curFood = currentGameState.getFood()
        curFoods = curFood.asList()
        ghostPositions = successorGameState.getGhostPositions() #next ghost state
        capsules = currentGameState.getCapsules()
        weight = 50
        totalscore = 0
        minDisToGhost = float("inf")
        ghostScared = newScaredTimes[0] > 0
        for ghost in ghostPositions:
            dis = util.manhattanDistance(ghost, newPos)
            minDisToGhost = min(dis, minDisToGhost)
            if (minDisToGhost <= 0):
                if (ghostScared):
                    totalscore += weight / 10
                else:
                    totalscore -= weight

        for capsule in capsules:
            dis = util.manhattanDistance(capsule, newPos)
            if (dis == 0):
                totalscore += weight
            else:
                totalscore += 2.0 / dis

        for foodPos in curFoods:
            dis = util.manhattanDistance(foodPos, newPos)
            if (dis == 0):
                totalscore += weight
            else:
                totalscore += 1.0 / dis

        return totalscore


def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"
        #util.raiseNotDefined()

        bestChoice = self.maximizer(gameState, self.depth)

        return bestChoice[1]

    def maximizer(self,state,curDepth):
        terminal = state.isWin() or state.isLose() or curDepth == 0
        if terminal:
          return self.evaluationFunction(state)
        avaibleActions=state.getLegalActions(self.index)
        values =[]
#        actions ={}
        for action in avaibleActions:
            values.append([self.minimizer(state.generateSuccessor(self.index,action),1, curDepth)])
#            value = self.minimizer(state.generateSuccessor(self.index,action),1, curDepth)
#            actions.setdefault(action,value)
            maxOptimalVal=max(values)
        for i in xrange(len(values)):
            if values[i] == maxOptimalVal:
               index = i
        maxDecision = (maxOptimalVal,avaibleActions[index])
        return maxDecision

    def minimizer(self, state, maximizers, curDepth):
        terminal = state.isWin() or state.isLose() or curDepth == 0
        if terminal:
            return self.evaluationFunction(state)
        avaibleActions = state.getLegalActions(maximizers)
        values = []
        for action in avaibleActions:
            if (maximizers +1 == state.getNumAgents()):
                values.append([self.maximizer(state.generateSuccessor(maximizers, action), (curDepth - 1))])
            else:
                values.append([self.minimizer(state.generateSuccessor(maximizers, action), maximizers + 1, curDepth)])
            minOptimal = min(values)
        for i in xrange(len(values)):
            if values[i] == minOptimal:
                index = i
        minDecision = (minOptimal, avaibleActions[index])
        return minDecision


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"

        numOfAgent = gameState.getNumAgents()
        numOfMinimizer = numOfAgent - 1
        alpha = [float("-inf")]
        betas = []
        for i in range(numOfMinimizer):
            betas.append(float("inf"))

        maxOptimal = float('-inf')
        terminal = gameState.isWin() or gameState.isLose()
        while not terminal:
            avaibleActions = gameState.getLegalActions(self.index)
            for action in avaibleActions:
                maxmizerOptimal = self.maxmizerOptimal(gameState.generateSuccessor(self.index, action), 1, alpha,betas)
                if maxmizerOptimal > maxOptimal:
                    maxmizerAction = action
                    maxOptimal = maxmizerOptimal
                alpha[0] = max(maxOptimal, alpha[0])
            return maxmizerAction
        return self.evaluationFunction(gameState)

    def maxmizerOptimal(self, gameState, curDepth, alpha, betas):
        terminal = gameState.isWin() or gameState.isLose() or curDepth == self.depth * gameState.getNumAgents()
        while not terminal:
            agentIndex = curDepth % gameState.getNumAgents()
            if  agentIndex > 0: # decide if the maximizer's turn or not
                alpha = alpha[:]
                betas = betas[:]
                minV = float('inf')
                for action in gameState.getLegalActions(agentIndex):
                    minV = min(minV, self.maxmizerOptimal(gameState.generateSuccessor(agentIndex, action), curDepth + 1,
                                                          alpha,betas))
                    if minV < alpha[0]:
                        return minV
                    betas[agentIndex - 1] = min(betas[agentIndex - 1], minV)
                return minV
            else:
                alpha = alpha[:]
                betas = betas[:]
                maxV = float('-inf')
                for action in gameState.getLegalActions(agentIndex):
                    maxV = max(maxV, self.maxmizerOptimal(gameState.generateSuccessor(agentIndex, action), curDepth + 1,
                                                          alpha,betas))
                    if maxV > min(betas):
                        return maxV
                    alpha[agentIndex] = max(alpha[agentIndex], maxV)
                return maxV
        return self.evaluationFunction(gameState)


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
 #       numOfAgent = gameState.getNumAgents()
 #       numOfMinimizer = numOfAgent - 1
 #       alpha = [float("-inf")]
 #       betas = []
 #       for i in range(numOfMinimizer):
 #           betas.append(float("inf"))

        maxOptimal = float('-inf')
        terminal = gameState.isWin() or gameState.isLose()
        while not terminal:
            avaibleActions = gameState.getLegalActions(self.index)
            for action in avaibleActions:
                maxmizerOptimal = self.maxmizerOptimal(gameState.generateSuccessor(self.index, action), 1)
                if maxmizerOptimal > maxOptimal:
                    maxmizerAction = action
                    maxOptimal = maxmizerOptimal
            return maxmizerAction
        return self.evaluationFunction(gameState)

    def maxmizerOptimal(self, gameState, curDepth):
        terminal = gameState.isWin() or gameState.isLose() or curDepth == self.depth * gameState.getNumAgents()
        while not terminal:
            agentIndex = curDepth % gameState.getNumAgents()
            if  agentIndex > 0: # decide if the maximizer's turn or not
                minV = 0
                avaibleActions = gameState.getLegalActions(agentIndex)
                for action in avaibleActions:
                    minV += (self.maxmizerOptimal(gameState.generateSuccessor(agentIndex, action), curDepth + 1))
                expV = minV / len(avaibleActions) * 100000
                return expV
            else:
                maxV = []
                avaibleActions = gameState.getLegalActions(agentIndex)
                for action in avaibleActions:
                    maxV.append(self.maxmizerOptimal(gameState.generateSuccessor(agentIndex, action), curDepth+1))
                maxOptimal = max(maxV)
                return maxOptimal
        return self.evaluationFunction(gameState)



def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"


    curPos = currentGameState.getPacmanPosition()
    curFood = currentGameState.getFood()
    curFoods = curFood.asList()
    newGhostStates = currentGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
    score = currentGameState.getScore()
    capsules = currentGameState.getCapsules()
    ghostScared = newScaredTimes[0] > 0
    weight = 10 ** 11
    distanceIni = 0
    foodDis = ghostDis = capsuleDis = distanceIni
    curGhost = []
    for ghost in newGhostStates:
        curGhost.append(ghost.getPosition())
    for pos in curGhost:
        ghostDis += util.manhattanDistance(curPos, pos)
    if ghostDis < 2:
        return -sys.maxint

    if  len(capsules) == 0 or not ghostScared:
        capsuleDis = sys.maxint
    else:
        if ghostDis > 2:
            moveToCapsule = sys.maxint
            for capsule in capsules:
                capsuleDis += util.manhattanDistance(capsule, curPos)
                while capsuleDis < moveToCapsule:
                    moveToCapsule = capsuleDis
        else:
            return -sys.maxint
# food
    moveToFood = (sys.maxint, sys.maxint)
    for foodPos in curFoods:
        distance = util.manhattanDistance(curPos, foodPos)
        foodDis += distance + 10
        while distance < util.manhattanDistance(curPos, moveToFood):
            moveToFood = foodPos
    while moveToFood == (sys.maxint, sys.maxint):
        if foodDis == 0:
            return (weight * score * score) / 500
        if foodDis == 1:
            return (weight * score * score) / 50
        if foodDis == 2:
            return (weight * score * score)/5
        if foodDis == 3:
            return (weight * score * score)
    moveToFood = util.manhattanDistance(curPos, moveToFood)

    heuristic = (weight/10000) /(capsuleDis + 100) + ((score * score * score)- 1000000) - \
                (200* (((foodDis * moveToFood) -100) /(ghostDis)))
    return heuristic




# Abbreviation
better = betterEvaluationFunction

