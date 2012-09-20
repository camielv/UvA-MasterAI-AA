# Assignment:   Single Agent Planning
# Course:       Autonomous Agents 2012-2013
# Education:    Master Artificial Intelligence
# By:           Steven Laan
#               Auke Wiggers
#               Camiel Verschoor
#
# File:         Prey.py
# Description:  Prey is a class containing properties of the prey, such as
#               the functions that enable movement. Prey is actually a part of 
#               the environment, but was implemented so that multiple preys 
#               would be possible in future assignments.

import random

class Prey():
    '''
    Creates an instance of prey. Input are an environment object and the 
    location of the prey in this environment, which is (5,5) by default.    
    '''

    ACTION_UP = (-1,0)
    ACTION_DOWN = (1,0)
    ACTION_RIGHT = (0,1)
    ACTION_LEFT = (0,-1)
    ACTION_STAY = (0,0)
    
    location = None
    actions = set([ACTION_UP, 
                   ACTION_DOWN, 
                   ACTION_RIGHT, 
                   ACTION_LEFT, 
                   ACTION_STAY])
    
    def __init__(self, environment, location):
        """
        Constructor defines movement probabilities
        """
        self.environment = environment
        self.location = location
    
    def simulateAction(self, s, reduced):
        """
        Function move(location, max_x, max_y) -> new_location
        
        Determines the new location of the prey based on the old location and
        the borders of the environment max_x,max_y.
        """        
 
        # Determine which function should be used based on a boolean 'reduced'.
        # If the boolean is true, the 2D state representation will be used. 
        if reduced:
            getPossibleStates = self.getPossibleStatesReduced
        else:
            getPossibleStates = self.getPossibleStates
        
        possible_states = getPossibleStates( s ) 
 
        # Between 0 and 1, used to determine the current action
        random_number = random.random()
        
        # Pick an action based on the number
        cumulative_prob = 0
        for s_prime in possible_states:
            cumulative_prob +=  possible_states[s_prime]
            if random_number <= cumulative_prob:
                if reduced:
                    new_x = self.location[0] + s[0] - s_prime[0]
                    new_y = self.location[1] + s[1] - s_prime[1]
                    
                    new_x = new_x % self.environment.width
                    new_y = new_y % self.environment.height
                    
                    self.location = (new_x, new_y)
                else:
                    self.location = (s_prime[2], s_prime[3])
                return s_prime
                
    def performAction(self, s, a):
        '''
        Perform a move given the current 4D state s and action a. Returns the 
        next 2D state.
        '''        
        old_x, old_y = s[2], s[3]        
        new_x = (old_x + a[0]) % self.environment.width
        new_y = (old_y + a[1]) % self.environment.height

        s_prime = (s[0], s[1], new_x, new_y)
        
        return s_prime

    def performActionReduced( self, s, a ):
        '''
        Perform a move given the current 2D state s and action a. Returns the 
        next 2D state.
        '''        
        old_x, old_y = s

        max_x = self.environment.width
        max_y = self.environment.height

        # There are, for this environment, 3 cases per dimension:
        if old_x > 0:
            # When the predator is not on the same vertical axis, an action can
            # be a move away from or towards the predator, or the prey can 
            # stand still
            new_x = ((old_x + 5 - a[0]) % max_x)-5
        elif old_x < 0:
            new_x = ((old_x + 5 + a[0]) % max_x)-5
        elif old_x == 0:
            # If the prey is already aligned, a moving action is always away
            # from the predator.
            new_x = a[0]
            
        # The same principle applies to moves in vertical direction. 
        if old_y > 0:
            new_y = ((old_y + 5 - a[1]) % max_y)-5
        elif old_y < 0:
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
            s_prime = self.performActionReduced( s, a )

            # check if the new prey location coincides with a predator
            if not s_prime in self.environment.terminal_states:
                possible_states[s_prime] = 1
        
        # find the probability of each move based on the possible moves 
        p_action = 0.2 / (len(possible_states) -1)
        for possible_s in possible_states:
            possible_states[possible_s] = p_action
        possible_states[s] = 0.8
        
        return possible_states
