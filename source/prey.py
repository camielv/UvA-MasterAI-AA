# Autonomous Agents - 2012/2013
# Team SuperAuke
#
# prey.py
# Base class for the prey

import random

class Prey():

    ACTION_UP = (-1,0)
    ACTION_DOWN = (1,0)
    ACTION_RIGHT = (0,1)
    ACTION_LEFT = (0,-1)
    ACTION_STAY = (0,0)
    
    location = None
    actions = set([ACTION_UP, ACTION_DOWN, ACTION_RIGHT, ACTION_LEFT, ACTION_STAY])
    
    def __init__(self, environment, location):
        """
        Constructor defines movement probabilities
        """
        self.environment = environment
        self.location = location
    
    def getLocation(self):
        return self.location    
    
    def simulateAction(self, s, reduced):
        """
        Function move(location, max_x, max_y) -> new_location
        
        Determines the new location of the prey based on the old location and
        the borders of the environment max_x,max_y.
        """        
 
        # Determine which function should be used based on a boolean 'reduced'.
        # If the boolean is true, the reduced statespace will be used. 
        if not reduced:
            getPossibleStates = self.getPossibleStates
            performAction = self.performAction
        else:
            getPossibleStates = self.getPossibleStatesReduced
            performAction = self.performActionReduced
        
        possible_states = getPossibleStates( s ) 
 
        # Between 0 and 1, used to determine the current action
        random_number = random.random()
        
        cumulative_prob = 0
        for a in possible_states:
            cumulative_prob +=  possible_states[a]
            if random_number <= cumulative_prob:
                self.location = performAction( s, a )
                return self.location
                
    def performAction(self, s, a):
        '''
        Perform a move given the current state        
        '''        
        old_x, old_y = s[2], s[3]        
        new_x = (old_x + a[0]) % self.environment.width
        new_y = (old_y + a[1]) % self.environment.height

        return (s[0], s[1], new_x, new_y)

    def performActionReduced( self, a, s ):
        ''' 
        Update the reduced state based on a given a. 
        '''
        d_x, d_y  = a
        
        old_x, old_y = s

        max_x = self.environment.width
        max_y = self.environment.height

        if old_x < 0:
            new_x = ((old_x + 5 - a[0]) % max_x)-5
        elif old_x > 0:
            new_x = ((old_x + 5 + a[0]) % max_x)-5
        elif old_x == 0:
            new_x = a[0]
            
        if old_y < 0:
            new_y = ((old_y + 5 - a[1]) % max_y)-5
        elif old_y > 0:
            new_y = ((old_y + 5 + a[1]) % max_y)-5
        elif old_y == 0:
            new_y = a[1]

        s_prime = (new_x, new_y)

        return s_prime

    def getPossibleStates( self, s ):
        '''
        Get the possible moves for a prey given the current state        
        '''
        possible_states = dict()
        if s in self.environment.terminal_states:
            possible_states[s] = 1
            return possible_states
            
        for a in self.actions:
            s_prime = self.performAction( s, a )
            if not s_prime in self.environment.terminal_states:
                possible_states[s_prime] = 1

        # find the probability of each move based on the possible moves 
        p_action = 0.2 / (len(possible_states)-1)
        for possible_s in possible_states:
            possible_states[possible_s] = p_action
        possible_states[s] = 0.8
        return possible_states

    def getPossibleStatesReduced(self, s ):
        '''
        Get the possible moves for a prey given the current reduced state     
        '''
        possible_states = dict()
        if s in self.environment.terminal_states:
            possible_states[s] = 1
            return possible_states

        for a in self.actions:            
            # determine the new location based on environment borders
            s_prime = self.performActionReduced( a, s )

            # check if the new prey location coincides with a predator
            if s_prime not in self.environment.terminal_states:
                possible_states[a] = 1
        
        # find the probability of each move based on the possible moves 
        for a in possible_states:
            possible_states[a] = 0.2 / len(possible_states)
        possible_states[s] = 0.8
        
        return possible_states
