# Assignment:   Single Agent Planning
# Course:       Autonomous Agents 2012-2013
# Education:    Master Artificial Intelligence
# By:           Steven Laan
#               Auke Wiggers
#               Camiel Verschoor
#
# File:         EnvironmentReduced.py
# Description:  Subclass of the environment, where a 2d state representation is
#               used.

from Environment import Environment

class EnvironmentReduced( Environment ):
    '''
    Creates an instance of the environment. Default an eleven by eleven grid
    is used. The default position for the prey is (5,5).
    '''
    #def __init__(self, preyLocation=(5,5), predatorLocation=(0,0) ):
    #    Environment.__init__(self)

    def getState(self):
        predator = self.predator.location
        prey = self.prey.location
        state_x = ( ( 5 + predator[0] - prey[0] ) % (self.width ) ) - 5
        state_y = ( ( 5 + predator[1] - prey[1] ) % (self.height ) ) - 5
        return state_x,state_y
    
    def getStates(self):
       '''
       Gets the entire statespace in two sets, the first containing the 
       non-terminal states and the second containing terminal states, 
       with reduced statespace. By taking distance to the prey in x- and 
       y-direction as the 2d state, the statespace is reduced by a factor 121. 
       '''
       S = set()
       terminal_states = set()
       for i in xrange( -(self.width/2), self.width/2+1 ):
           for j in xrange( -(self.height/2), self.height/2+1 ):
                s = (i,j)         
                if i == 0 and j == 0:
                    terminal_states.add( s )
                else:
                    S.add( s )

       return S, terminal_states

    def reward( self, s, a, s_prime ):
        '''
        Returns the reward for a given 2d future state, where (0,0) stands 
        for zero distance from predator to prey. In this case, state and 
        action are actually redundant but are added for the sake of 
        completeness.
        '''
        if (s_prime[0], s_prime[1]) == (0, 0):
            return 10
        return 0

    def nextStates( self, s, a ):
        '''
        Determine the next possible states given the current state and 
        action the predator takes.         
        '''
        new_state = self.predator.performActionReduced( s, a )
        return self.prey.getPossibleStatesReduced( new_state )
        
        
    def run( self ):
        '''Performs one step of the simulation.'''
        # Retrieve the state
        s = self.getState()
        
        # Update predator positions given a state s
        s_prime = self.predator.simulateAction( s, True )
            
        # Update prey position given the new state
        self.prey.simulateAction( s_prime, True )