# valueIterationAgents.py
# -----------------------
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


import mdp, util

from learningAgents import ValueEstimationAgent
import sys

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0

        # Write value iteration code here
        "*** YOUR CODE HERE ***"
        times = self.iterations
        states = self.mdp.getStates()
        while (times != 0):
            V = util.Counter()
            for state in states:
                if not self.mdp.isTerminal(state):
                    optimal = -sys.maxint
                    actions = self.mdp.getPossibleActions(state)
                    for action in actions:
                        totalValue = 0
                        stateProPairs = self.mdp.getTransitionStatesAndProbs(state,action)
                        for stateProPair in stateProPairs:
                            rVknextstate = self.discount * self.values[stateProPair[0]]
                            reward = self.mdp.getReward(state,action,stateProPair[0])
                            totalValue += stateProPair[1] * (reward + rVknextstate)
                        optimal = max(totalValue, optimal)
                        V[state] = optimal
                else:
                    V[state] = 0
            times -= 1
            self.values = V

    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]


    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        "*** YOUR CODE HERE ***"
 #       util.raiseNotDefined()
        totalValue = 0
        stateProbPairs = self.mdp.getTransitionStatesAndProbs(state,action)
        for stateProbPair in stateProbPairs:
            rVknextstate = self.discount * self.values[stateProbPair[0]]
            reward = self.mdp.getReward(state,action,stateProbPair[0])
            totalValue += stateProbPair[1] * ( reward + rVknextstate)
        return totalValue


    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
                      if qV > optimalV:
                optimalV = qV
                decision = action
        """
        "*** YOUR CODE HERE ***"
 #       util.raiseNotDefined()
        while self.mdp.isTerminal(state):
            return None

        Actions = self.mdp.getPossibleActions(state)

        valuesForActions = util.Counter()
        decision = "north"
        optimalV = -sys.maxint
        actionQ = {}
        for action in Actions:
         #   stateProbPairs = self.mdp.getTransitionStatesAndProbs(state, action)
            qV = self.computeQValueFromValues(state, action)
            actionQ [action] = qV
        decision =max(actionQ.items(), key=lambda x: x[1])[0]

        return decision

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)
