# Assignment:   Single Agent Planning
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
        self.environment = environment
        # For every non-terminal state in the statespace, determine the 
        # possible actions and their probabilities.
        for s in self.environment.S:
            for a in self.actions:
                self.policy[(s,a)] = 0.2
                    
    def simulateAction( self, s, reduced ):
        '''
        Perform an action based on the policy, given the s
        '''
        
        # Determine which function should be used based on a boolean 'reduced'.
        # If the boolean is true, the reduced sspace will be used.
        if not reduced:
            performAction = self.performAction
        else:
            performAction = self.performActionReduced
        
        a = self.getAction( s ) 
        print 'predator move:', a
        
        s_prime = performAction( s, a )

        # If the 2D staterepresentation is used instead of the 4D one
        if reduced:          
            # Use a different method to update the state
            new_x = self.location[0] - (s[0] - s_prime[0])
            new_y = self.location[1] - (s[1] - s_prime[1])
            
            new_x = new_x % self.environment.width
            new_y = new_y % self.environment.height
            self.location = (new_x, new_y)
        else:
            self.location = (s_prime[0], s_prime[1])
        return s_prime

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
        Update the location based on a given action, regardless of policy. 
        '''
        x,y = s[0],s[1]
        
        new_x = (x + a[0]) % self.environment.width
        new_y = (y + a[1]) % self.environment.height
       
        return ( new_x, new_y, s[2], s[3] )

    def performActionReduced( self, s, a ):
        ''' 
        Update the location based on a given action. Reduced s version. 
        '''
        d_x, d_y  = a
        old_x, old_y = s

        max_x = self.environment.width
        max_y = self.environment.height

        # There are, for this environment, 3 cases per dimension:
        if old_x < 0:
            # If the predator is not on the same y-axis as the prey, a move
            # in horizontal direction will be either towards or away from 
            # the prey, or a standstill.
            new_x = ((old_x + 5 + a[0]) % max_x)-5
        elif old_x > 0:
            new_x = ((old_x + 5 - a[0]) % max_x)-5
        elif old_x == 0:
            # If it is on the same y-axis, any action in horizontal direction 
            # will be a move away from the prey.
            new_x = -a[0]
            
        # The same principle applies to moves in vertical direction
        if old_y < 0:
            new_y = ((old_y + 5 + a[1]) % max_y)-5
        elif old_y > 0:
            new_y = ((old_y + 5 - a[1]) % max_y)-5
        elif old_y == 0:
            new_y = -a[1]

        return (new_x, new_y)

    def updatePolicy(self, s, best_a):
        '''
        Given a state and the best action, this function sets the predators 
        policy so that in state s, the probability of taking action best_a is
        1.0 and probabilities of taking any other actions are (of course) 0. 
        '''
        # Set probabilities of all actions to 0
        for a in self.actions:
            self.policy[(s,a)] = 0.0
            
        # Give the new action for this state a probability of 1
        self.policy[(s,best_a)] = 1.0
        
