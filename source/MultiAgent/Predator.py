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
    
    def updateQ(self, s, a, s_prime, r):
        self.QLearning.updateQ( s, a, s_prime, r )
    