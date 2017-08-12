# search.py
# ---------
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

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"
#    util.raiseNotDefined()
    #print "Start:", problem.getStartState()
    #print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    #print "Start's successors:", problem.getSuccessors(problem.getStartState())
    frontier = util.Stack()
    frontier.push((problem.getStartState(), "", 0))
    explored = []
    relationships = {}
    while frontier:
        node = frontier.pop()
        explored.append(node[0])
        if problem.isGoalState(node[0]):
            return actions(node, relationships)
        successors = problem.getSuccessors(node[0])
        for succ in successors:
            if (succ[0] not in explored) and (succ not in frontier.list):
               relationships[succ] = node
               frontier.push(succ)
    return "no solution"

def actions (goal, relationships):
    from game import Directions
    action = []
    node = goal
    while(node[1]):
#        actions.append(relationships[node][1])
        action.append(node[1])
        node = relationships[node]
    action.reverse()
#    print("Path:", action)
    return action

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    frontier = util.Queue()
    frontier.push((problem.getStartState(), "", 0))
    explored = []
    relationships = {}
    while frontier:
        node = frontier.pop()
        explored.append(node[0])
        if problem.isGoalState(node[0]):
            return actions(node, relationships)
        successors = problem.getSuccessors(node[0])
        for succ in successors:
            if (succ[0] not in explored) and (succ[0] not in [x[0] for x in frontier.list]):
               relationships[succ] = node
               frontier.push(succ)
    return "no solution"

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    frontier = util.PriorityQueueWithFunction(lambda x : x[2])
    frontier.push((problem.getStartState(), "", 0))
    statefrontier =[(problem.getStartState)]
    explored = []
    relationships = {}
    totalCost = {}
    totalCost[problem.getStartState()] = 0
    while frontier:
        node = frontier.pop()
        statefrontier.pop()
        explored.append(node[0])
        if problem.isGoalState(node[0]):
            return actions(node, relationships)
        successors = problem.getSuccessors(node[0])
        for succ in successors:
            if (succ[0] in totalCost) and (totalCost[succ[0]] > node[2] + succ[2])\
                    or ((succ[0] not in explored) and (succ[0] not in statefrontier)):
                newCost = node[2] + succ[2]
                totalCost[succ[0]] = newCost
                frontier.push((succ[0], succ[1], newCost))
                statefrontier.append(succ[0])
                relationships[(succ[0], succ[1], newCost)] = node

    return "no solution"


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"

    frontier = util.PriorityQueue()
    frontier.push((problem.getStartState(), "", 0), 0)
    statefrontier = [problem.getStartState]
    relationships = {}
    explored =[]
    totalCost = {}
    totalCost[problem.getStartState()] = 0
    while frontier:
        node = frontier.pop()
        statefrontier.pop()
        explored.append(node[0])
        if problem.isGoalState(node[0]):
            return actions(node, relationships)
        successors = problem.getSuccessors(node[0])
        for succ in successors:
            if ((succ[0] not in explored) and (succ[0] not in statefrontier)):
                pCost = succ[2] + node[2]
                dCost = heuristic(succ[0],problem)
                frontier.push((succ[0],succ[1],pCost), pCost + dCost)
                totalCost[succ[0]] = pCost
                statefrontier.append(succ[0])
                relationships[(succ[0], succ[1], pCost)] = node
            elif ((succ[0] in statefrontier) and (totalCost[succ[0]] > succ[2] + node[2])):
                pCost = succ[2] + node[2]
                dCost = heuristic(succ[0],problem)
                frontier.push((succ[0],succ[1],pCost), pCost + dCost)
                totalCost[succ[0]] = pCost
                statefrontier.append(succ[0])
                relationships[(succ[0], succ[1], pCost)] = node
    return "no solutions"


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
