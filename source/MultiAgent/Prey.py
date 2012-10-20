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
from random import random 

class Prey( Agent ):
    '''
    Creates an instance of prey. Input are an environment object and the 
    location of the prey in this environment, which is (5,5) by default.    
    '''

    def updateQ(self, s, a, s_prime, r):
        self.QLearning.updateQ( s, a, s_prime, -r )
        
    def performAction( self, a ):
        ''' 
        s_prime <- performAction( a )        
        
        Update the location of an agent based on a given action a. Trips with
        probability 0.2.
        '''
        if random() > 0.2:
            old_x, old_y = self.location
    
            new_x = (old_x + a[0]) % self.Environment.width
            new_y = (old_y + a[1]) % self.Environment.height
            
            self.location = (new_x, new_y)
    