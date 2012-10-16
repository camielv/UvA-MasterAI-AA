# Assignment:   MultiAgent Planning/Learning
# Course:       Autonomous Agents 2012-2013
# Education:    Master Artificial Intelligence
# By:           Steven Laan
#               Auke Wiggers
#               Camiel Verschoor
#
# File:         QLearning.py
# Description:  Implementation of Q-learning

import time    
import random
from itertools import izip
    
argmax = lambda d: max( izip( d.itervalues(), d.iterkeys() ) )[1]    
    
class QLearning():
    '''    
    Implementation of functions related to Q-learning.    
    '''
    
    def __init__(self, Agent, alpha, gamma, epsilon, optimistic_value=5):
        '''
        Fill all values of Q based on a given optimistic value.
        '''
        # Set the agent for this QLearning session
        self.Agent = Agent
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon

        # Value of any nonterminal state is the optimistic value
        self.Q = dict()
        for s in self.Agent.Environment.S:
            self.Q[s] = dict()            
            for a in self.Agent.actions:
                self.Q[s][a] = optimistic_value

        # Value of absorbing state(s) is 0
        for s in self.Agent.Environment.terminal_states:
            self.Q[s] = dict()            
            for a in self.Agent.actions:
                self.Q[s][a] = 0    

        
    def updateQ(self, s, a, s_prime, r):
        '''
        Perform one step for this agent for a given state s. Action, resulting
        state s_prime, and observed reward r are also given.         
        '''
        # Determine which action maximizes Q(s,a)
        max_Q = self.Q[s_prime][argmax( self.Q[s_prime] )]
        
        # Update Q
        self.Q[s][a] += self.alpha * (r + self.gamma * max_Q - self.Q[s][a])
       