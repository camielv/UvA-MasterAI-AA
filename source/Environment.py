# Assignment:   Single Agent Planning
# Course:       Autonomous Agents 2012-2013
# Education:    Master Artificial Intelligence
# By:           Steven Laan
#               Auke Wiggers
#               Camiel Verschoor
#
# File:         environment.py
# Description:  Base class of the environment.

class Environment:
    '''
    Creates an instance of the environment. Default an eleven by eleven grid
    is used. The default position for the prey is (5,5).
    '''
    def __init__( self, width=11, height=11 ):
        self.width  = width
        self.height = height
        self.S, self.terminal_states = self.getStates()        

    def getState( self ):
        '''Returns the current environment state.'''
        
        raise NotImplementedError
        
    def getStates(self):
        '''
        Gets the entire statespace in two sets, the first containing the non-
        terminal states and the second containing terminal states.
        '''
        raise NotImplementedError

    def policyEvaluation(self):
        '''
        Performs policyEvaluation for the given predator in this environment. 
        '''

        V = dict()
        # For every state in the statespace including terminal states
        for s in self.S | self.terminal_states:
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
                    P = self.nextStates( s, a )
                    for s_prime in P:
                        new_V[s] += policy[(s,a)] * P[s_prime] * ( self.reward( s, a, s_prime ) + discount * V[s_prime] )
                        
                # Compute the error
                delta = max( delta, abs( V[s] - new_V[s] ) )
         
            # Store the new values
            V.update( new_V )
            
            i += 1

        print 'Iteration', i
        return V

    def reward( self, s, a, s_prime ):
        '''
        Returns the reward for a given future 4d state containing location of 
        the predator and prey. In this case, state and action are actually 
        redundant but are added for the sake of completeness. 
        '''
        raise NotImplementedError

    def nextStates( self, s, a ):
        raise NotImplementedError
          
    def valueIteration( self ):    
        ''' 
        Perform value iteration for this environment. 
        '''        
        
        V = dict()
        for s in self.S | self.terminal_states:
            V[s] = 0
          
        policy = self.predator.policy # Returns a dict

        # Define delta and theta
        delta = 0.2  
        theta = 0.00 
        discount = 0.7
        new_V = dict()
            
        # Policy evaluation
        while delta > theta:
            delta = 0
            for s in self.S:
                new_V[s] = 0                     
                
                best_value = None
                best_action = None
                
                for a in self.predator.actions:
                    current_value = 0
                    policy[ (s, a) ] = 0
                    
                    # Calculate all next states and their probabilities
                    P = self.nextStates( s, a )
                    
                    # Find the action that maximizes the value
                    for s_prime in P:
                        current_value +=  P[s_prime] * ( self.reward( s, a, s_prime ) + discount * V[s_prime] )
                
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
        
    def policyIteration( self ):
        '''
        Performs policy iteration starting from the policy of the predator.
        '''
        # Initialization
        stable = False
        gamma = 0.7
        
        while not stable:
            # Policy evaluation
            V = self.policyEvaluation()
            
            # Policy improvement
            stable = True
            for s in self.S:
                # Retrieve action according to policy
                policy_action = self.predator.getAction( s )
                
                best_action = None
                best_value = None
                
                # Check all possible actions
                for a in self.predator.actions:
                    P = self.nextStates( s, a )
                    value = 0
                    
                    for s_prime in P:
                        value += P[s_prime] * ( self.reward( s, a, s_prime ) + gamma * V[s_prime] )
                        
                    if value > best_value:
                        best_action = a
                
                # Check policy stability
                if best_action != policy_action:
                    self.predator.updatePolicy( s, best_action )
                    stable = False

    def run( self ):
        '''Performs one step of the simulation.'''
        # Retrieve the state
        s = self.getState()
        print s
        
        # Update predator positions given a state s
        new_state = self.predator.simulateAction( s, False )

            
        # Update prey position given the new state
        s_prime = self.prey.simulateAction( s, False )
