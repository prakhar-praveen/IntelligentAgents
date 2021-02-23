# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util, sys, math

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
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
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
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        foodList = newFood.asList()
        minFoodMDistance = sys.maxsize
        ghostLocationsList = successorGameState.getGhostPositions()
        for _ in foodList: minFoodMDistance = min(minFoodMDistance, util.manhattanDistance(newPos, _))
        for gpos in ghostLocationsList:
            if (util.manhattanDistance(newPos, gpos) < 2):
                return - float("inf")
        return successorGameState.getScore() + 1.0/minFoodMDistance

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

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        return self.minimaxHelperFunction(gameState, 1, 0 )
        #Since there is only one Pacman_Agent (agent0) out of all agents in the game
        #number of ghosts will be numAgents - 1
    def minimaxHelperFunction(self, gameState, curr_depth, agentIndex):
        if gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
        elif curr_depth > self.depth:
            return self.evaluationFunction(gameState)

        legalActions = []
        for _ in gameState.getLegalActions(agentIndex):
            if _ != 'Stop':
                legalActions.append(_)

        nextIndex = agentIndex + 1
        nextDepth = curr_depth

        if nextIndex >= gameState.getNumAgents():
            nextIndex = 0
            nextDepth += 1


        optimal_action_indexes = []
        optimal_actions = []

        for _ in legalActions:
            optimal_actions.append(self.minimaxHelperFunction(gameState.generateSuccessor(agentIndex, _), nextDepth, nextIndex))
        #pacman moves for the first time
        if agentIndex == 0 and curr_depth == 1:
            maxMove = max(optimal_actions)
            for i in range(len(optimal_actions)):
                if optimal_actions[i] == maxMove:
                    optimal_action_indexes.append(i)
            # return action of randomly
            return legalActions[random.choice(optimal_action_indexes)]

        if agentIndex == 0: return max(optimal_actions)
        else: return min(optimal_actions)


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """
    def maximize(self, gameState, depth, agentIndex, numGhosts, alpha, beta):
        """
          maximizing agent with alpha-beta pruning
        """
        if gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
        maximum = -sys.maxsize
        optimal_action = Directions.STOP

        for _ in gameState.getLegalActions(agentIndex):
            nextGameState = gameState.generateSuccessor(agentIndex, _)

            currMax = self.minimize(nextGameState, depth, 1, numGhosts, alpha, beta)

            if currMax >  maximum:
                maximum = currMax
                optimal_action = _

            if maximum > beta: return maximum
            alpha = max(alpha, maximum)
        if agentIndex == 0 and depth > 1: return maximum
        return optimal_action

    def minimize(self, gameState, depth, agentIndex, numGhosts, alpha, beta):
        """
          minimizing agent with alpha-beta pruning
        """
        if gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
        minimum = sys.maxsize
        for _ in gameState.getLegalActions(agentIndex):
            nextGameState = gameState.generateSuccessor(agentIndex, _)
            if depth < self.depth and agentIndex == numGhosts: currMin = self.maximize(nextGameState, depth + 1, 0, numGhosts, alpha, beta)
            elif agentIndex == numGhosts and not depth < self.depth: currMin = self.evaluationFunction(nextGameState)
            else: currMin = self.minimize(nextGameState, depth, agentIndex + 1, numGhosts, alpha, beta)

            if currMin == min(currMin, minimum): minimum = currMin

            if agentIndex is not 0 and minimum < alpha: return minimum
            else: beta = min(beta, minimum)
        return minimum

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        if gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
        #0 as in pacman (agent0)  agentindex = 0 for maximizing  (pacman) agent
        return self.maximize(gameState, 1, 0, gameState.getNumAgents() - 1, float("-inf"), float("inf"))

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
        return
        util.raiseNotDefined()
    def expectimaxHelper(self, gameState, currentDepth, agentIndex):
        if gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
        elif currentDepth > self.depth:
            return self.evaluationFunction(gameState)

        legalActions = []
        for _ in gameState.getLegalActions(agentIndex):
            if _ != 'Stop':
                legalActions.append(_)

        nextIndex = agentIndex + 1
        nextDepth = currentDepth

        if nextIndex >= gameState.getNumAgents():
            nextIndex = 0
            nextDepth += 1



        optimal_actions = []

        optimal_action_indexes = []
        for _ in legalActions:
            optimal_actions.append(self.expectimaxHelper(gameState.generateSuccessor(agentIndex, _), nextDepth, nextIndex))
        #pacman moves for the first time
        if agentIndex == 0 and currentDepth == 1:
            maxMove = max(optimal_actions)
            for i in range(len(optimal_actions)):
                if optimal_actions[i] == maxMove:
                    optimal_action_indexes.append(i)
            # return action of randomly
            return legalActions[random.choice(optimal_action_indexes)]

        if agentIndex == 0: return max(optimal_actions)
        else:
            "In ghost node, return the average(expected) value of action"
            return sum(legalActions)/len(legalActions)
