# Assignment:   MultiAgent Planning/Learning
# Course:       Autonomous Agents 2012-2013
# Education:    Master Artificial Intelligence
# By:           Steven Laan
#               Auke Wiggers
#               Camiel Verschoor
#
# File:         Predator.py
# Description:  Predator is a class containing properties of the agent.

from Agent import Agent

class Predator( Agent ):
    '''
    Creates an agent which contains a policy. Input are an environment object
    and the location of the agent, which is (0,0) by default.    
    '''

    def performAction( self, a ):
        ''' 
        performAction( a )        
        
        Update the location of an agent based on a given action a.
        '''
        old_x, old_y = self.location

        new_x = (old_x + a[0]) % self.Environment.width
        new_y = (old_y + a[1]) % self.Environment.height
        
        self.location = (new_x, new_y)

    
    def updateQ( self, s, a, s_prime, r ):
        '''
        updateQ( s, a, s_prime, r )

        Given the old state s, an action this agent took, the new state s_prime
        and the reward for going to this new state, update Q.
        '''
        self.QLearning.updateQ( s, a, s_prime, r )
    