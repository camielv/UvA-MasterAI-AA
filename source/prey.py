# Autonomous Agents - 2012/2013
# Team SuperAuke
#
# prey.py
# Base class for the prey

import random

class Prey():

    MOVE_UP = (-1,0)
    MOVE_DOWN = (1,0)
    MOVE_RIGHT = (0,1)
    MOVE_LEFT = (0,-1)
    MOVE_STAY = (0,0)
    
    location = (0,0)    
    
    def __init__(self, location):
        """
        Constructor defines movement probabilities
        """
        self.location = location
    
    def getLocation(self):
        return self.location    
    
    def move(self, max_x, max_y, state):
        """
        Function move(location, max_x, max_y) -> new_location
        
        Determines the new location of the prey based on the old location and
        the borders of the environment max_x,max_y.
        """        
        possible_moves = self.getPossibleMoves(max_x, max_y, state)

        # Between 0 and 1, used to determine the current action
        random_number = random.random()
        
        cumulative_prob = 0
        for move in possible_moves:
            cumulative_prob += self.prob_move[move]
            if random_number <= self.prob_move:
                old_x, old_y = self.location
                # determine the new location based on environment borders
                new_x = (old_x + move[0]) % max_x
                new_y = (old_y + move[1]) % max_y

                new_prey_location = (new_x, new_y)

                self.location = new_prey_location
                
    def hypoMove(self, max_x, max_y, state, move):
        old_x, old_y = state[2], state[3]        
        new_x = (old_x + move[0]) % max_x
        new_y = (old_y + move[1]) % max_y

        return (state[0], state[1], new_x, new_y)

    def hypoMoveReduced( self, max_x, max_y, action, state ):
        ''' Update the location based on a given action. '''
        d_x, d_y  = action
        
        old_x, old_y = state

        if old_x < 0:
            new_x = ((old_x + 5 - action[0]) % max_x)-5
        elif old_x > 0:
            new_x = ((old_x + 5 + action[0]) % max_x)-5
        elif old_x == 0:
            new_x = action[0]
            
        if old_y < 0:
            new_y = ((old_y + 5 - action[1]) % max_y)-5
        elif old_y > 0:
            new_y = ((old_y + 5 + action[1]) % max_y)-5
        elif old_y == 0:
            new_y = action[1]

        newstate = (new_x, new_y)
        return newstate


    def getPossibleMoves(self, max_x, max_y, state):
        possible_moves = dict()
        for move in [self.MOVE_UP, self.MOVE_DOWN, self.MOVE_RIGHT, self.MOVE_LEFT]:
            old_x, old_y = state[2], state[3]
            # determine the new location based on environment borders
            new_x = (old_x + move[0]) % max_x
            new_y = (old_y + move[1]) % max_y

            # check if the new prey location coincides with a predator
            if (new_x,new_y) == (state[0], state[1]):
                continue
            else:
                # this beautiful pythonian for-else construction triggers the
                # else if the for loop is ended normally (not by break). 
                possible_moves[move] = 1

        # find the probability of each move based on the possible moves 
        if len(possible_moves) > 0:
            for move in possible_moves:
                possible_moves[move] = 0.2 / len(possible_moves)        
        possible_moves[self.MOVE_STAY] = 0.8
        return possible_moves

    def getPossibleMovesReduced(self, max_x, max_y, state):
        possible_moves = dict()
        for move in [self.MOVE_UP, self.MOVE_DOWN, self.MOVE_RIGHT, self.MOVE_LEFT]:
            
            # determine the new location based on environment borders
            new_state = self.hypoMoveReduced(max_x, max_y, move, state)

            new_x, new_y = new_state

            # check if the new prey location coincides with a predator
            if new_state == (0,0):
                continue
            else:
                possible_moves[move] = 1

        
        # find the probability of each move based on the possible moves 
        for move in possible_moves:
            possible_moves[move] = 0.2 / len(possible_moves)
        possible_moves[self.MOVE_STAY] = 0.8
        return possible_moves

