# Assignment:   Single Agent Planning
# Course:       Autonomous Agents 2012-2013
# Education:    Master Artificial Intelligence
# By:           Steven Laan
#               Auke Wiggers
#               Camiel Verschoor
#
# File:         environment.py
# Description:  Base class of the environment.

from predator import Predator
from prey import Prey

class Environment:
    '''
    Creates an instance of the environment. Default an eleven by eleven grid
    is used. The default position for the prey is (5,5).
    '''
    def __init__(self, width=11, height=11, preyLocation=(5,5), 
                 predatorLocation=(0,0) ):
        self.width  = width
        self.height = height
        S,terminal_states = self.getStates()        
        self.S = S
        self.terminal_states = terminal_states
                
        
        self.predator = Predator( self, predatorLocation )
        self.prey = Prey( self, preyLocation )
        
    def getState( self ):
        '''Returns the current environment state.'''
        # Create state
        predator_x, predator_y = self.predator.getLocation()
        prey_x, prey_y = self.prey.getLocation()
        
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
                        s = (i,j,k,m)                 
                        if i == k and j == m:
                            terminal_states.add( s )
                        else:
                            S.add( s )
        return S, terminal_states

    def getStatesReduced(self):
       '''
       Gets the entire statespace in two sets, the first containing the non-terminal states and the second containing terminal states, with reduced statespace. By taking distance to the prey in x- and y-direction as the 2d state, the statespace is reduced by a factor 121. 
       '''
       S = set()
       terminal_states = set()
       for i in xrange( self.width ):
           for j in xrange( self.height ):
                s = (i,j)         
                if i == 0 and j == 0:
                    terminal_states.add( s )
                else:
                    S.add( s )

       return S, terminal_states

    def policyEvaluation(self, reduced=False):
        '''
        Performs policyEvaluation for the given predator in this environment. 
        '''

        # Initialize the variables that will keep track of all states S and their valuesV
        if not reduced:
            reward = self.reward
            nextStates = self.nextStates
        else:
            reward = self.rewardReduced
            nextStates = self.nextStatesReduced

        V = dict()
        # For every state in the statespace including terminal states
        for s in self.S.union( self.terminal_states ):
            V[s] = 0
          
        # Get the current policy 
        policy = self.predator.policy 

        # Define delta and theta
        delta = 0.2 
        theta = 0   
        discount = 0.8
        # Keep track of the number of iterations
        i = 0
        
        # Policy evaluation
        while delta > theta:
            delta = 0
            new_V = dict()
           
            for s in self.S:
                new_V[s] = 0               
               
                for a in self.predator.actions:
                    # Calculate all next states and their probabilities
                    P = nextStates( s, a )
                      
                    for s_prime in P:
                        new_V[s] += policy[(s,a)] * P[s_prime] * ( reward( s, a, s_prime ) + discount * V[s_prime] )
                # Compute the error
                delta = max( delta, abs( V[s] - new_V[s] ) )
         
            # Store the new values
            V.update( new_V )
            
            i += 1

        print 'Iteration', i

    def reward( self, s, a, s_prime ):
        '''
        Returns the reward for a given future 4d state containing location of 
        the predator and prey. In this case, state and action are actually 
        redundant but are added for the sake of completeness. 
        '''
        print s_prime
        if (s_prime[0], s_prime[1]) == (s_prime[2], s_prime[3]):
            return 10
        return 0

    def rewardReduced( self, s, a, s_prime ):
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
        new_state = self.predator.performAction( s, a )
        return self.prey.getPossibleActions( new_state )
          
    def nextStatesReduced( self, s, a ):
        new_state = self.predator.performActionReduced( s, a )
        return self.prey.getPossibleActionsReduced( new_state )
        
    def valueIteration( self, reduced=False ):    
        ''' 
        Perform value iteration for this environment. 
        '''        
        
        # Initialize the variables that will keep track of all states S and their values V
        if reduced:
            reward = self.rewardReduced
            nextStates = self.nextStatesReduced
        else:
            reward = self.reward
            nextStates = self.nextStates

        V = dict()
        for s in self.S.union( self.terminal_states ):
            V[s] = 0
          
        policy = self.predator.policy # Returns a dict
        # Define delta and theta
        delta = 0.2  
        theta = 0.001   
        
        # Policy evaluation
        while delta > theta:
            delta = 0
            new_V = dict()
            discount = 0.8
            for s in self.S:
                new_V[s] = 0                     
                
                best_value = None
                best_action = None
                
                for a in self.predator.actions:
                    current_value = 0
                    policy[ (s, a) ] = 0
                    
                    # Calculate all next states and their probabilities
                    P = nextStates( s, a )
                    
                    # Find the action that maximizes the value
                    for s_prime in P:
                        current_value +=  P[s_prime] * ( reward( s, a, s_prime ) + discount * V[s_prime] )
                
                    if current_value > best_value:
                        best_value = current_value
                        best_action = a
                        
                # In the new policy, that action is now the only one that is taken
                policy[ ( s, best_action ) ] = 1.0           
                new_V[s] = best_value
                
                # Compute the error
                delta = max( delta, abs( V[s] - new_V[s] ) )
        
            # Store the new values
            V.update( new_V )
        return V

    def run( self ):
        '''Performs one step of the simulation.'''
        # Retrieve the state
        s = self.getState()
        
        # Update predator positions given a state s
        new_state = self.predator.simulateMove( self.width, self.height, s )

            
        # Update prey position given the new state
        s_prime = self.prey.simulateMove( self.width, self.height, new_state )