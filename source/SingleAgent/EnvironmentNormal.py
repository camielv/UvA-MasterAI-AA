# Assignment:   Single Agent Planning
# Course:       Autonomous Agents 2012-2013
# Education:    Master Artificial Intelligence
# By:           Steven Laan
#               Auke Wiggers
#               Camiel Verschoor
#
# File:         environment.py
# Description:  Subclass of the environment.

from Environment import Environment

class EnvironmentNormal( Environment ):
    '''
    Creates an instance of the environment. Default an eleven by eleven grid
    is used. The default position for the prey is (5,5).
    '''
    
    def getState( self ):
        '''
        Returns the current environment state.
        '''
        # Create state
        predator_x, predator_y = self.predator.location
        prey_x, prey_y = self.prey.location
        
        # Retrieve predator positions
        s = (predator_x, predator_y, prey_x, prey_y)
        
        return s
        
    def getStates(self):
        '''
        Gets the entire statespace in two sets, the first containing the non-terminal states and the second containing terminal states.
        '''
        S = set()
        terminal_states = set() 
        for i in xrange( self.width ):
            for j in xrange( self.height ):
                for k in xrange( self.width ):
                    for m in xrange( self.height ):
                        s = (i, j, k, m)                 
                        if i == k and j == m:
                            terminal_states.add( s )
                        else:
                            S.add( s )
        return S, terminal_states
    
    def reward( self, s, a, s_prime ):
        '''
        Returns the reward for a given future 4d state containing location of 
        the predator and prey. In this case, state and action are actually 
        redundant but are added for the sake of completeness. 
        '''
        if (s_prime[0], s_prime[1]) == (s_prime[2], s_prime[3]):
            return 10
        return 0

    def nextStates( self, s, a ):
        '''
        Determines all possible next states s' given the current state s and 
        action a.         
        '''
        new_state = self.predator.performAction( s, a )
        return self.prey.getPossibleStates( new_state )
        
    def run( self ):
        '''
        Performs one step of the simulation.
        '''
        # Retrieve the state
        s = self.getState()
        
        # Update predator positions given a state s
        s_prime = self.predator.simulateAction( s, False )
            
        # Update prey position given the new state
        self.prey.simulateAction( s_prime, False )