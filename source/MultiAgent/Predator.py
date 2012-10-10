# Assignment:   MultiAgent Planning/Learning
# Course:       Autonomous Agents 2012-2013
# Education:    Master Artificial Intelligence
# By:           Steven Laan
#               Auke Wiggers
#               Camiel Verschoor
#
# File:         Predator.py
# Description:  Predator is a class containing properties of the agent, such as
#               the policy, as well as functions that enable movement.

import random
from math import exp
from QLearning import QLearning

class Predator():
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
        self.location = location
        self.Environment = environment
        self.QLearning = QLearning( self )        
        
        # For every non-terminal state in the statespace, determine the 
        # possible actions and their probabilities.
        for s in self.Environment.S:
            for a in self.actions:
                self.policy[(s,a)] = 0.2
    
    def takeAction( self, s, a ):
        ''' 
        Perform one step for this predator.
        '''
        # Udpate the state based on the predator's action
        s_new = self.performAction(s, a)
        # Choose an action for the prey
        s_prime = self.Environment.Prey.simulateAction( s_new, reduced=True )
        # Determine the reward for the state-action-next_state pair
        r = self.Environment.reward(s, a, s_prime)
        # Check if the found state is terminal
        terminal = s_prime in self.Environment.terminal_states

        return r, s_prime, terminal
        
            
    def simulateAction( self, s ):
        '''       
        s_prime <- simulateAction( s )

        Perform an action based on the policy, given the state s.
        Returns the resulting next state s_prime. 
        '''
        
        a = self.getAction( s ) 
        s_prime = self.performAction( s, a )

        # Update the state
        new_x = self.location[0] - (s[0] - s_prime[0])
        new_y = self.location[1] - (s[1] - s_prime[1])
        
        new_x = new_x % self.Environment.width
        new_y = new_y % self.Environment.height
        self.location = (new_x, new_y)

        return s_prime
