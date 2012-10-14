# Assignment:   Single Agent Planning
# Course:       Autonomous Agents 2012-2013
# Education:    Master Artificial Intelligence
# By:           Steven Laan
#               Auke Wiggers
#               Camiel Verschoor
#
# File:         Prey.py
# Description:  Prey is a class containing properties of the prey.

from Agent import Agent
import random

class Prey( Agent ):
    '''
    Creates an instance of prey. Input are an environment object and the 
    location of the prey in this environment, which is (5,5) by default.    
    '''
    
    def performAction( self, a ):
        ''' 
        performAction( a )        
        
        Update the location of an agent based on a given action a, with a 0.2
        chance of tripping.
        '''
        old_x, old_y = self.location

        # The move succeeds with probability 0.8
        if random.random() > 0.2:
            new_x = (old_x + a[0]) % self.Environment.width
            new_y = (old_y + a[1]) % self.Environment.height
            self.location = (new_x, new_y)
            
    def updateQ( self, s, a, s_prime, r ):
        '''
        updateQ( s, a, s_prime, r )

        Given the old state s, an action this agent took, the new state s_prime
        and the reward for going to this new state, update Q.
        
        The prey has a reward of -r (since r is the reward for team predator).        
        '''
        self.QLearning.updateQ( s, a, s_prime, -r )