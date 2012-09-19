# Autonomous Agents - 2012/2013
# Team SuperAuke
#
# predator.py
# Base class for the predator (agent)

import random

class Predator():
    
    ACTION_UP    = (-1, 0)
    ACTION_DOWN  = ( 1, 0)
    ACTION_RIGHT = ( 0, 1)
    ACTION_LEFT  = ( 0,-1)
    ACTION_STAY  = ( 0, 0)   
    
    actions = set([ACTION_UP, ACTION_DOWN, ACTION_RIGHT, ACTION_LEFT, ACTION_STAY])
    policy = dict()
    
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
        
        return performAction( s, a )

    def getAction( self, s ):
        '''
        Get an action given the current state, using the policy
        '''
        random_number = random.random()

        cumulative_prob = 0 
        
        for a in self.policy:
            cumulative_prob += self.policy[a]
            if cumulative_prob > random_number:                
                return a

    def performAction( self, s, a ):
        ''' 
        Update the location based on a given action, regardless of policy. 
        '''
        x,y = s[0],s[1]
        
        new_x = (x + a[0]) % self.environment.width
        new_y = (y + a[1]) % self.environment.height
       
        return ( s[0], s[1], new_x, new_y )

    def performActionReduced( self, s, a ):
        ''' 
        Update the location based on a given action. Reduced s version. 
        '''
        d_x, d_y  = a
        old_x, old_y = s

        max_x = self.environment.width
        max_y = self.environment.height

        if old_x < 0:
            new_x = ((old_x + 5 + a[0]) % max_x)-5
        elif old_x > 0:
            new_x = ((old_x + 5 - a[0]) % max_x)-5
        elif old_x == 0:
            new_x = -a[0]
            
        if old_y < 0:
            new_y = ((old_y + 5 + a[1]) % max_y)-5
        elif old_y > 0:
            new_y = ((old_y + 5 - a[1]) % max_y)-5
        elif old_y == 0:
            new_y = -a[1]

        return (new_x, new_y)
