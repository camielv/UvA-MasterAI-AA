# Assignment:   MultiAgent Planning/Learning
# Course:       Autonomous Agents 2012-2013
# Education:    Master Artificial Intelligence
# By:           Steven Laan
#               Auke Wiggers
#               Camiel Verschoor
#
# File:         Agent.py
# Description:  Agent is an abstract class 

from QLearning import QLearning

import random
from iteritems import izip

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

    def __init__( self, environment, location=(0,0) ):        
        self.Environment = environment
        self.location = location
        self.QLearning = QLearning( self )        
        
        # For every non-terminal state in the statespace, determine the 
        # possible actions and their probabilities (random at first).
        for s in self.Environment.S:
            for a in self.actions:
                self.policy[(s,a)] = 0.2


    def deriveAction( self, s ):
        '''
        Find an action using the current state and Q, in an 
        epsilon-greedy fashion. 
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
        Get an action given the current state, using the policy. 
        '''
        random_number = random.random()

        cumulative_prob = 0.0
        
        # For every action, check if the cumulative probability exceeds a 
        # random number. 
        for a in self.actions:
            cumulative_prob += self.policy[(s,a)]
            if cumulative_prob >= random_number:                
                return a

    def performAction( self, s, a ):
        ''' 
        s_prime <- performAction( s, a )        
        
        Find the next state s_prime based on a given action a and the current 
        state s. Return that next state.
        '''
        d_x, d_y  = a
        old_x, old_y = s

        max_x = self.Environment.width
        max_y = self.Environment.height

        # There are, for this environment, 3 cases per dimension:
        if old_x < 0:
            # If the predator is not on the same y-axis as the prey, a move
            # in horizontal direction will be either towards or away from 
            # the prey, or a standstill.
            new_x = ((old_x + 5 - a[0]) % max_x)-5
        elif old_x > 0:
            new_x = ((old_x + 5 - a[0]) % max_x)-5
        elif old_x == 0:
            # If it is on the same y-axis, any action in horizontal direction 
            # will be a move away from the prey.
            new_x = -a[0]
            
        # The same principle applies to moves in vertical direction
        if old_y < 0:   
            new_y = ((old_y + 5 - a[1]) % max_y)-5
        elif old_y > 0:
            new_y = ((old_y + 5 - a[1]) % max_y)-5
        elif old_y == 0:
            new_y = -a[1]

        return (new_x, new_y)

