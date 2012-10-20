# Assignment:   MultiAgent Planning/Learning
# Course:       Autonomous Agents 2012-2013
# Education:    Master Artificial Intelligence
# By:           Steven Laan
#               Auke Wiggers
#               Camiel Verschoor
#
# File:         QLearning.py
# Description:  Implementation of Q-learning

from itertools import izip
from collections import defaultdict
import numpy

argmax = lambda d: max( izip( d.itervalues(), d.iterkeys() ) )[1]    
    
class QLearning():
    '''    
    Implementation of functions related to Q-learning.    
    '''
    
    def __init__(self, 
                 Agent, 
                 alpha, 
                 gamma, 
                 epsilon, 
                 optimistic_value=5):
        '''
        Fill all values of Q based on a given optimistic value.
        '''

        # Set the agent for this QLearning session
        self.Agent = Agent
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon

        default = lambda : dict(zip([action for action in self.Agent.actions],
                                    [numpy.float(0.0) for action in self.Agent.actions]))

        self.Q = defaultdict(default)
        self.optimistic_value = optimistic_value        


                    
    def updateQ(self, s, a, s_prime, r):
        '''
        Perform one step for this agent for a given state s. Action, resulting
        state s_prime, and observed reward r are also given.         
        '''        
        max_Q = self.Q[s_prime][argmax( self.Q[s_prime] )]

        
        # Update Q. Q[s][a] should already be known to us.
        self.Q[s][a] += self.alpha * (r + self.gamma * max_Q - self.Q[s][a])