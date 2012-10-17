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

        self.Q = dict()
        self.optimistic_value = optimistic_value        
        
    def initQ(self, s):
        '''
        initQ( s )        
        
        Add entry s to the Q matrix, based on the optimistic initial value.
        '''        
        
        self.Q[s] = dict()
        if (0,0) in s or len(set(s)) != len(s):
            for action in self.Agent.actions:
                self.Q[s][action] = 0
                
        else:
            for action in self.Agent.actions:
                self.Q[s][action] = self.optimistic_value

            
    def updateQ(self, s, a, s_prime, r):
        '''
        Perform one step for this agent for a given state s. Action, resulting
        state s_prime, and observed reward r are also given.         
        '''        
        # If needed, initialize Q[s]
        if not s_prime in self.Q:        
            self.initQ(s_prime)
        
        max_Q = self.Q[s_prime][argmax( self.Q[s_prime] )]
        
        # Update Q. Q[s][a] should already be known to us.
        self.Q[s][a] += self.alpha * (r + self.gamma * max_Q - self.Q[s][a])
       
