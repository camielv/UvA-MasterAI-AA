# Autonomous Agents - 2012/2013
# Team SuperAuke
#
# playingField.py
# Base Class for the playingfield
from predator import Predator
from prey import Prey
from copy import deepcopy

class Environment:
    
    '''
    Creates an instance of the environment. Default an eleven by eleven grid
    is used. The default position for the prey is (5,5).
    '''
    
    def __init__( self, width = 11, height = 11, preyLocation = (5,5), predatorLocation = (0,0) ):
        self.width  = width
        self.height = height
        self.predator = Predator( predatorLocation )
        self.prey = Prey( preyLocation )
        
        self.caught = False
    
    def getWidth( self ):
        '''Returns the width of the environment.'''
        return self.width
    
    def getHeight( self ):
        '''Returns the height of the environment.'''
        return self.height

    def policyEvaluation(self):
       
        # Define the set of actions
        actions = set( [ (0,0),(1,0), (0,1), (-1,0), (0,-1) ] )
                  
        # Define the discount
        discount = 0.8

        # Define the set of all states
        S = set( [ (i,j) for i in range(self.width) for j in range(self.height) ] )

        # Define the policy (currently random: 5 actions per state, each prob(a) = 0.2)
        policy = dict()
        for s in S:
            for a in actions:
                policy[(s,a)] = 0.2
        
        # Define delta and theta
        delta = 0.2   
        theta = 0.01    
        
        # Define dictionaries for the Value-function
        V = dict()    
        new_V = dict()    
        
        # Initialize the Value function to zero
        for s in S: 
            V[s] = 0    
        
        # Policy evaluation
        while delta > theta:
            delta = 0
            
            for s in S:
                new_V[s] = 0
                v = V[s]                        
                
                for a in actions:
                    # Calculate all next states and their probabilities
                    next_states, P = self.nextStates( s, a )
                    
                    for next_state in next_states:
                        new_V[s] += policy[(s,a)] * P[next_state] * ( self.reward( next_state ) + discount * V[next_state] )
                
                # Compute the error
                delta = max( delta, abs( v - new_V[s] ) )

            # Store the new values
            V = deepcopy(new_V)
            
        return V

    def reward( self, state ):
        
        if (state[0],state[1]) == (0,0):
            return 10
        return 0

    def nextStates( self, state, action ):
        '''
        Returns a tuple containing a list of all possible next states and a
        dictionary containing the transition probabilities of those next states.
        '''
        # Determine the new location based on environment borders
        new_state = self.predator.hypoMoveReduced(self.width, self.height, action, state)
       
        moves = self.prey.getPossibleMovesReduced( self.getWidth(), self.height, new_state )

        next_states = list()
        P = dict()

        for move in moves:
            # Determine the next state based on the move of the prey
            next_state = self.prey.hypoMoveReduced(self.width, self.height, new_state, move)
            next_states.append(next_state)
            P[next_state] = moves[move]
        
        return next_states, P

    def getReducedState( self ):
        '''Returns the current state in a more concise manner: uses only 
        relative position of the predator with respect to the prey. '''
        prey_x, prey_y = self.prey.getLocation() 
        width =  self.width            
        height = self.height        
            
        x,y = self.predator.getLocation()            
            
        dist_x = min((x-prey_x) % width, (x+prey_x) % width)
        dist_y = min((y-prey_y) % width, (y+prey_y) % width)
            
        state = (dist_x, dist_y)

        return state
            
    
    def run( self ):
        '''Performs one step of the simulation.'''
        # Retrieve the state
        state = self.getReducedState()
        
        # Update predator positions
        if self.predator.moveReduced( self.width, self.height, state, self.preyLocation ):
            self.caught = True
            return
            
        # Update prey position
        self.prey.moveReduced( self.width, self.height, state, self.preyLocation )
