# Autonomous Agents - 2012/2013
# Team SuperAuke
#
# playingField.py
# Base Class for the playingfield
from predator import Predator
from prey import Prey

class Environment:
    
    '''
    Creates an instance of the environment. Default an eleven by eleven grid
    is used. The default position for the prey is (5,5).
    '''
    
    def __init__( self, width = 11, height = 11, preyLocation = (5,5) ):
        self.width  = width
        self.height = height
        self.predators = []
        self.prey = Prey( preyLocation )
        
        self.caught = False
    
    def getWidth( self ):
        '''Returns the width of the environment.'''
        return self.width
    
    def getHeight( self ):
        '''Returns the height of the environment.'''
        return self.height
    
    def addPredator( self, location ):
        '''Adds a predator to the environment at the given location.'''
        newPredator = Predator( location )
        self.predators.append( newPredator )
    
    def getState( self ):
        '''Returns the current environment state.'''
        # Create state
        state = dict()
        state['predator'] = []
        state['prey'] = self.prey.getLocation()
        
        # Retrieve predator positions
        for predator in self.predators:
            state['predator'].append( predator.getLocation() )
        
        return state
        
    def getReducedState( self ):
        '''Returns the current state in a more concise manner: uses only 
        relative position of the predator with respect to the prey. '''
        prey_x, prey_y = self.prey.getLocation() 
        width =  self.getWidth()            
        height = self.getHeight()        
        
        state = dict()
        state['predator'] = list()
        for predator in self.predators:
            
            x,y = predator.getLocation()            
            
            dist_x = (x-prey_x) % width
            dist_y = (x-prey_y) % height
            
            state['predator'].append( (dist_x, dist_y) )
    
    def run( self ):
        '''Performs one step of the simulation.'''
        # Retrieve the state
        state = self.getState()
        
        # Update predator positions
        for predator in self.predators:
            if predator.move( self.width, self.height, state ):
                self.caught = True
                return
            
        # Update prey position
        self.prey.move( self.width, self.height, state )