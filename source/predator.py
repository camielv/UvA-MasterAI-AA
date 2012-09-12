# Autonomous Agents - 2012/2013
# Team SuperAuke
#
# predator.py
# Base class for the predator (agent)

import random

class Predator():
    
    MOVE_UP    = (-1, 0)
    MOVE_DOWN  = ( 1, 0)
    MOVE_RIGHT = ( 0, 1)
    MOVE_LEFT  = ( 0,-1)
    MOVE_STAY  = ( 0, 0)   
    
    location = (0,0)
    
    def __init__( self, location ):
        self.location = location
    
    def getLocation( self ):
        return self.location
    
    def randomMove( self, max_x, max_y ):
        random_number = random.random()
        prob_move = {self.MOVE_UP: 0.2,
                     self.MOVE_DOWN: 0.2,
                     self.MOVE_RIGHT: 0.2,
                     self.MOVE_LEFT: 0.2,
                     self.MOVE_STAY: 0.2}
        cumulative_prob = 0 
        
        for move in prob_move:

            cumulative_prob += prob_move[move]

            if cumulative_prob > random_number:                
                
                #print move 
                old_x, old_y = self.location
                # determine the new location based on environment borders
                new_x = (old_x + move[0]) % max_x
                new_y = (old_y + move[1]) % max_y
                
                self.location = (new_x, new_y)

    def hypoMoveReduced( self, max_x, max_y, action, state ):
        ''' Update the location based on a given action. '''
        d_x, d_y  = action
        old_x, old_y = state

        if old_x < 5:
            new_x = (old_x + action[0]) % max_x
        elif old_x > 5:
            new_x = (old_x - action[0]) % max_x
        elif old_x == 5:
            new_x = min((old_x - action[0]) % max_x, (old_x + action[0]) % max_x)
            
        if old_y < 5:
            new_y = (old_y + action[0]) % max_y
        elif old_y > 5:
            new_y = (old_y - action[0]) % max_y
        elif old_y == 5:
            new_y = min((old_y - action[0]) % max_y, (old_y + action[0]) % max_y)

        newstate = (new_x, new_y)
        return newstate

        
