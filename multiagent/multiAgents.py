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
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        dist_pellet = []
        currFood = currentGameState.getFood()
        for pellet in currFood.asList():
            if action == Directions.STOP:
                return -float("inf")

            if manhattanDistance(pellet, newPos) == 0:
                dist_pellet.append(0.5)
            else:
                dist_pellet.append(manhattanDistance(pellet, newPos))
        for ghost in newGhostStates:
            if manhattanDistance(newPos, ghost.getPosition()) == 0:
                return -float("inf")
        dist_pellet_shortest = 1/min(dist_pellet)
        return currentGameState.getScore() + dist_pellet_shortest


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
        def minimax(gameState, agentIndex, depth):
            result = []

            if gameState.isLose() or gameState.isWin() or depth == self.depth:
                return self.evaluationFunction(gameState), 0

            if agentIndex == gameState.getNumAgents() - 1:
                depth += 1
                next_agent = self.index
            else:
                next_agent = agentIndex + 1

            for action in gameState.getLegalActions(agentIndex):
                if not result:
                    next_value = minimax(gameState.generateSuccessor(agentIndex, action), next_agent, depth)
                    result.append(next_value[0])
                    result.append(action)
                else:
                    previous_value = result[0]
                    next_value = minimax(gameState.generateSuccessor(agentIndex, action), next_agent, depth)

                    if agentIndex == self.index:
                        if next_value[0] > previous_value:
                            result[0] = next_value[0]
                            result[1] = action
                    else:
                        if next_value[0] < previous_value:
                            result[0] = next_value[0]
                            result[1] = action
            return result

        return minimax(gameState, self.index, 0)[1]


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

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
        def expectimax(gameState, agentIndex, depth):
            result = []

            if gameState.isLose() or gameState.isWin() or depth == self.depth:
                return self.evaluationFunction(gameState), 0

            if agentIndex == gameState.getNumAgents() - 1:
                depth += 1
                next_agent = self.index

            else:
                next_agent = agentIndex + 1

            for action in gameState.getLegalActions(agentIndex):
                if not result:
                    next_value = expectimax(gameState.generateSuccessor(agentIndex, action), next_agent, depth)

                    if agentIndex != self.index:
                        result.append((1.0 / len(gameState.getLegalActions(agentIndex))) * next_value[0])
                        result.append(action)
                    else:
                        result.append(next_value[0])
                        result.append(action)
                else:
                    previous_value = result[0]
                    next_value = expectimax(gameState.generateSuccessor(agentIndex, action), next_agent, depth)

                    if agentIndex == self.index:
                        if next_value[0] > previous_value:
                            result[0] = next_value[0]
                            result[1] = action
                    else:
                        result[0] = result[0] + (1.0 / len(gameState.getLegalActions(agentIndex))) * next_value[0]
                        result[1] = action
            return result

        return expectimax(gameState, self.index, 0)[1]

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <Incomplete function, partially wrote code that I felt was needed but did not know how to implement
      this function. I just added ghosts and distances into lists according to their state and respective distances.>
    """
    "*** YOUR CODE HERE ***"
    food = currentGameState.getFood().asList()
    ghosts = currentGameState.getGhostStates()
    pacman_pos = currentGameState.getPacmanPosition()
    active_ghosts = []
    scared_ghosts = []

    for ghost in ghosts:
        if ghost.scaredTimer:
            scared_ghosts.append(ghost)
        else:
            active_ghosts.append(ghost)

    food_distances = []
    active_ghosts_distances = []
    scared_ghosts_distances = []

    for x in food:
        food_distances.append(manhattanDistance(pacman_pos, x))

    for x in active_ghosts:
        active_ghosts_distances.append(manhattanDistance(pacman_pos, x.getPosition()))

    for x in scared_ghosts:
        scared_ghosts_distances.append(manhattanDistance(pacman_pos, x.getPosition()))


# Abbreviation
better = betterEvaluationFunction

