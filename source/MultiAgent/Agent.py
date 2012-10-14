# Assignment:   MultiAgent Planning/Learning
# Course:       Autonomous Agents 2012-2013
# Education:    Master Artificial Intelligence
# By:           Steven Laan
#               Auke Wiggers
#               Camiel Verschoor
#
# File:         Agent.py
# Description:  Agent is an abstract class 

import random
from itertools import izip
from QLearning import QLearning

argmax = lambda d: max( izip( d.itervalues(), d.iterkeys() ) )[1]    

class Agent():
    '''
    Creates an agent which contains a policy. Input are an environment object
    and the location of the agent, which is (0,0) by default.    
    '''
    ACTION_UP    = (-1, 0)
    ACTION_DOWN  = ( 1, 0)
    ACTION_RIGHT = ( 0, 1)
    ACTION_LEFT  = ( 0,-1)
    ACTION_STAY  = ( 0, 0)   
    
    actions = set([ACTION_UP, ACTION_DOWN, ACTION_RIGHT, ACTION_LEFT, ACTION_STAY])
    policy = dict()
    location = None

    def __init__( self, environment, location=(0,0), policy=None):        
        
        self.Environment = environment
        self.location = location
        self.QLearning = QLearning( self,  0.5, 0.7, 0.1, 5 )        
        
        # For every non-terminal state in the statespace, determine the 
        # possible actions and their probabilities (random at first).
        if policy:
            self.policy = policy
        else:
            for s in self.Environment.S:
                for a in self.actions:
                    self.policy[(s,a)] = 1.0 / len(self.actions)

    def getActionEpsilonGreedy( self, s ):
        '''
        a <- getActionEpsilonGreedy(s)
        
        Find an action using the current state s, in an epsilon-greedy fashion. 
        '''
        # Find the action that maximizes Q[(s, a)]                
        prob_actions = dict()        
        uniform_epsilon = self.QLearning.epsilon / (len(self.actions))
        
        for possible_a in self.actions:
            # Set probabilities of all actions uniformly
            prob_actions[possible_a] = uniform_epsilon
        
        # Give the best action for this state a probability of 1
        best_a = argmax( self.QLearning.Q[s] )
            
        prob_actions[best_a] += 1 - self.QLearning.epsilon
                    
        # For every action, check if the cumulative probability exceeds a 
        # random number. 
        random_number = random.random()
        cumulative_prob = 0.0
        
        for a in self.actions:
            cumulative_prob += prob_actions[a]
            if cumulative_prob >= random_number:                
                return a
    
    def getAction( self, s ):
        '''
        a <- getAction(s)        
        
        Get an action given the current state s, using the policy. 
        '''
        random_number = random.random()

        cumulative_prob = 0.0
        
        # For every action, check if the cumulative probability exceeds a 
        # random number. 
        for a in self.actions:
            cumulative_prob += self.policy[(s,a)]
            if cumulative_prob >= random_number:                
                return a

    def performAction( self, a ):
        raise NotImplementedError        
        
    def updateQ(self, s, a, s_prime, r):
        raise NotImplementedError