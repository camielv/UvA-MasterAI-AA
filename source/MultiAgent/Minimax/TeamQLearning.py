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
        self.policy = dict()
        self.Q = dict()
        self.V = dict()
        S = set( [ (i,j) for i in range(-5,6) for j in range(-5,6)] )
        for s in S:
            self.V[s] = numpy.float16( 0 )
            self.Q[s] = dict()
            self.policy[s] = dict()
            
            for a in self.Agent.actions:
                self.policy[s][a] = numpy.float16( 1.0 / len( self.Agent.actions ) )
                
                for o in self.Agent.actions:
                    self.Q[s][(a,o)] = numpy.float16( 0.0 )
                    
    def updateQ(self, s, a, o, s_prime, r):
        '''
        Perform one step for this agent for a given state s. Action, resulting
        state s_prime, and observed reward r are also given.         
        '''        
        # Update Q. Q[s][a] should already be known to us.
        self.Q[s][(a,o)] = (1-self.alpha) * self.Q[s][(a,o)] + \
                           self.alpha * (r + self.gamma * self.V[s_prime])
            
        self.V[s] = self.Q[s][(a,o)]
 