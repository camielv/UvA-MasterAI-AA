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
    
class TeamQLearning():
    '''    
    Implementation of functions related to Q-learning.    
    '''
    
    def __init__(self, 
                 Agent, 
                 alpha, 
                 gamma, 
                 epsilon):
        '''
        Fill all values of Q based on a given optimistic value.
        '''

        # Set the agent for this QLearning session
        self.Agent = Agent
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon

        defaultdefault = lambda : numpy.float(0.0)
        default = lambda : defaultdict(defaultdefault)

        self.Q = defaultdict(default)
        self.V = defaultdict(defaultdefault)
                    
    def updateQ(self, s, a, o, s_prime, r):
        '''
        Perform one step for this agent for a given state s. Action, resulting
        state s_prime, and observed reward r are also given.         
        '''        
        # Update Q. Q[s][a] should already be known to us.
        self.Q[s][(a,o)] = (1-self.alpha) * self.Q[s][(a,o)] + \
                           self.alpha * (r + self.gamma * self.V[s_prime])
                           
        self.TeamQLearning.V[s] = min( self.TeamQLearning.Q[s] )
 