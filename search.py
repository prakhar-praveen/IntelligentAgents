# search.py
# ---------
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


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    #trivial case-- Start state == goal state
    start_state = problem.getStartState()
    if problem.isGoalState(start_state):
        return []

    #Implementing our Depth-first Search using stack
    fringe_stack = util.Stack()

    #Using (current_node,action) tuple
    #where action contains list of actions
    #aka path of actions
    #to get to the current node
    #which corresponds to the current state
    #in the state space

    # pushing current (node, actions) tuple
    # action is empty for start node
    actionList = []
    fringe_stack.push((start_state,actionList))

    #Initializing set for storing visited nodes
    visited_set = set()
    #Adding start state to visited set because it's been visited(added to the stack)
    visited_set.add(start_state)

    #Depth-first Search:
    while fringe_stack:
        node_curr,actions_list = fringe_stack.pop()

        #Checking if current node has been already expanded
        #If not, adding it to visited_set
        if node_curr not in visited_set:
            visited_set.add(node_curr)
            #If curr node/state is Goal state, return the actions
            if problem.isGoalState(node_curr):
                return actions_list
            else:
                #Iterating through the list of successors given by the getSuccessors funtion
                #every successor returned by the function is a triple (successor,action, stepCost)
                for successor_node,action,step_cost in problem.getSuccessors(node_curr):
                    fringe_stack.push((successor_node,actions_list + [action]))
        else:
            if problem.isGoalState(node_curr):
                return actions_list
            else:
                #Iterating through the list of successors given by the getSuccessor funtion
                #every successor returned by the function is a triple (successor,action, stepCost)
                for successor_node,action,step_cost in problem.getSuccessors(node_curr):
                    fringe_stack.push((successor_node,actions_list + [action]))
    util.raiseNotDefined()

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    #similar implementation to the DFS implementation above
    #so reusing the skeleton from above

    #trivial case-- Start state == goal state
    start_state = problem.getStartState()
    if problem.isGoalState(start_state):
        return []

    #BFS using Queue:
    #Implementing our Breadth-first Search using Queue, initialized below
    fringe_queue = util.Queue()

    #Using (current_node,action) tuple
    #where action contains list of actions
    #aka path of actions
    #to get to the current node
    #which corresponds to the current state
    #in the state space

    # pushing current state and actions (node, actions) tuple
    # action is empty for start node
    actionList = []
    fringe_queue.push((start_state,actionList))

    #Initializing set for storing visited nodes
    visited_set = set()
    #Adding start state to visited set because it's been visited and added to the stack
    visited_set.add(start_state)

    #Breadth-first Search:
    while fringe_queue:
        node_curr,actions_list = fringe_queue.pop()

        #Checking if current node has been already expanded
        #If not, adding it to visited_set
        if node_curr not in visited_set:
            visited_set.add(node_curr)
            #If curr node/state is Goal state, return the actions
            if problem.isGoalState(node_curr):
                return actions_list
            else:
                #Iterating through the list of successors given by the getSuccessor funtion
                #every successor returned by the function is a triple (successor,action, stepCost)
                for successor_node,action,step_cost in problem.getSuccessor(node_curr):
                    fringe_queue.push((successor_node,actions_list + [action]))
        else:
            #If curr node/state is Goal state, return the actions
            if problem.isGoalState(node_curr):
                return actions_list
            else:
                #Iterating through the list of successors given by the getSuccessor funtion
                #every successor returned by the function is a triple (successor,action, stepCost)
                for successor_node,action,step_cost in problem.getSuccessors(node_curr):
                    fringe_queue.push((successor_node,actions_list + [action]))
    util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    #trivial case: Start state == goal state
    startState = problem.getStartState()
    if problem.isgoalState(startState):
        return []
    #Implementing Uniform-cost Search using Priority Queue
    #becuase we choose to priorize based on cost

    #Defining and Initializing a Priority Queue
    fringe_priority_queue = util.PriorityQueue()

    #Using (node, action, currStepCost), nextStepCost) tuple
    #for storing info of every state
    #Pushing first Start State
    fringe_priority_queue.push((startState,[],0),0)
    # pushing start state (start_node, actionList, currStepCost), nextStepCost)
    # where actionList is empty for start node, currStepCost = 0, nextStepCost

    #Initializing set for storing visited nodes
    visited_set = set()
    #Adding start state to visited set because it's been visited and added to the stack
    visited_set.add(problem.getStartState())

    #Uniform-cost Search:
    while fringe_priority_queue:
        node_curr, actions_list, cost = fringe_priority_queue.pop()
        #Checking if current node has been already expanded
        #If not, adding it to visited_set
        if node_curr not in visited_set:
            visited_set.add(node_curr)
            #If curr node/state is Goal state, return the actions
            if problem.isGoalState(node_curr):
                return actions_list
            else:
                #Iterating through the list of successors given by the getSuccessor funtion
                #every successor returned by the function is a 3-tuple (successor,action, stepCost)
                for successor_node,action,step_cost in problem.getSuccessors(node_curr):
                    nextAction = actions_list + [action]
                    nextStepCost = problem.getCostOfActions(nextAction)
                    fringe_priority_queue.push((successor_node,nextAction,step_cost),nextStepCost)
    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    startState = problem.getStartState()
    #trivial case: Start state == goal state
    if problem.isGoalState(startState):
        return []
    #Implementing A* Search using Priority Queue
    #becuase we are still prioritizing searching based on cost
    #just like UCS, although we need to take into account heuristic too

    #Defining and Initializing a Priority Queue
    fringe_priority_queue = util.PriorityQueue()
    #Using (node, action, currStepCost), nextStepCost) tuple
    #for storing info of every state
    #Pushing first Start State
    fringe_priority_queue.push((startState,[],0),0)
    # pushing start state (start_node, actionList, currStepCost), nextStepCost)
    # where actionList is empty for start node, currStepCost = 0, nextStepCost

    #Initializing set for storing visited nodes
    visited_set = set()
    #Adding start state to visited set because it's been visited and added to the stack
    visited_set.add(problem.getStartState())

    #A* Search:
    while fringe_priority_queue:

        node_curr, actions_list, cost = fringe_priority_queue.pop()
        #Checking if current node has been already expanded
        #If not, adding it to visited_set
        if node_curr not in visited_set:

            visited_set.add(node_curr)

            #If curr node/state is Goal state, return the actions
            if problem.isGoalState(node_curr):
                return actions_list

            else:
                #Iterating through the list of successors given by the getSuccessors funtion
                #every successor returned by the function is a 3-tuple (successor,action, stepCost)
                for successor_node,action,step_cost in problem.getSuccessors(node_curr):
                    nextAction = actions_list + [action]
                    nextStepCost = problem.getCostOfActions(nextAction)
                    heuristicCost = nextStepCost + heuristic(successor_node,problem)
                    fringe_priority_queue.push((successor_node,nextAction,step_cost),nextStepCost)
    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch

