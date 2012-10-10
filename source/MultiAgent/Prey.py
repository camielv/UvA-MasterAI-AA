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

class Prey( Agent ):
    '''
    Creates an instance of prey. Input are an environment object and the 
    location of the prey in this environment, which is (5,5) by default.    
    '''

    def updateQ(self, s, a, s_prime, r):
        self.QLearning.updateQ( s, a, s_prime, -r )