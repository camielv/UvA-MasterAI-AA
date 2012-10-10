# Assignment:   Single Agent Learning
# Course:       Autonomous Agents 2012-2013
# Education:    Master Artificial Intelligence
# By:           Steven Laan
#               Auke Wiggers
#               Camiel Verschoor
#
# File:         environment.py
# Description:  Base class of the environment.
from Predator import Predator
from Prey import Prey

import time

class Environment:
    '''
    Creates an instance of the environment. Default an eleven by eleven grid
    is used. The default position for the prey is (5,5).
    '''
    def __init__( self, 
                  width=11, 
                  height=11, 
                  preyLocation=(5,5), 
                  predatorLocation=(0,0),
                  numberOfPredators=1  ):
                      
        assert numberOfPredators > 0
        assert numberOfPredators < 5
        assert type(numberOfPredators) == int        
        
        self.width  = width
        self.height = height
        self.S,self.terminal_states = self.getStates()

        self.Prey = Prey( self, preyLocation )
        self.PredatorLocations = [(0,0), (10,0), (0,10), (10,10)]

        self.Predators = [Predator(self, self.predatorLocations[i]) \
                          for i in range(numberOfPredators)]        
    
                        
                
    def getState( self ):
        '''Returns the current environment state.'''        
        raise NotImplementedError
        
    def getStates(self):
        '''
        Gets the entire statespace in two sets, the first containing the non-
        terminal states and the second containing terminal states.
        '''
        raise NotImplementedError

    def reward( self, s, a, s_prime ):
        '''
        Returns the reward for a given future 4d state containing location of 
        the predator and prey. In this case, state and action are actually 
        redundant but are added for the sake of completeness. 
        '''
        raise NotImplementedError

    def nextStates( self, s, a ):
        raise NotImplementedError
          
    def policyEvaluation( self, gamma = 0.8 ):
        '''
        Performs policyEvaluation for the given predator in this environment. 
        '''
        
        V = dict()
        # For every state in the statespace including terminal states
        for s in self.S | self.terminal_states:
            V[s] = 0
          
        # Get the current policy 
        policy = self.Predator.policy

        # Define delta and theta
        delta = 0.2
        theta = 0   
        
        # Keep track of the number of iterations
        i = 0
        
        # Policy evaluation
        while delta > theta:
            delta = 0
            new_V = dict()
           
            for s in self.S:
                new_V[s] = 0               
               
                for a in self.Predator.actions:
                    # Calculate all next states and their probabilities
                    P = self.nextStates( s, a )
                    for s_prime in P:
                        new_V[s] += policy[(s,a)] * P[s_prime] * ( self.reward( s, a, s_prime ) + gamma * V[s_prime] )
                        
                # Compute the error
                delta = max( delta, abs( V[s] - new_V[s] ) )
         
            # Store the new values
            V.update( new_V )
            
            i += 1

        print 'Policy Evaluation took', i, 'iterations'
        return V

    def valueIteration( self, gamma = 0.7 ):    
        ''' 
        Perform value iteration for this environment. 
        '''        
        now = time.time()
        
        iterations = 0        
        
        V = dict()
        for s in self.S | self.terminal_states:
            V[s] = 0
        
        # Define delta and theta
        delta = 0.2  
        theta = 0.0

        new_V = dict()
            
        # Policy evaluation
        while delta > theta:
            iterations += 1
            delta = 0
            for s in self.S:
                new_V[s] = 0                     
                
                best_value = None
                best_action = None
                
                for a in self.Predator.actions:
                    current_value = 0
                    
                    # Calculate all next states and their probabilities
                    P = self.nextStates( s, a )
                    
                    # Find the action that maximizes the value
                    for s_prime in P:
                        current_value +=  P[s_prime] * ( self.reward( s, a, s_prime ) + gamma * V[s_prime] )
                
                    if current_value > best_value:
                        best_value = current_value
                        best_action = a
                        
                # In the new policy, that action is now the only one that is taken
                self.Predator.updatePolicy( s, best_action )
                new_V[s] = best_value
                
                # Compute the error
                delta = max( delta, abs( V[s] - new_V[s] ) )
        
            # Store the new values
            V.update( new_V )
        print 'Number of iterations for discount', gamma, ' :', iterations
        print 'Time taken (seconds): ', time.time() - now
        return V        
        
    def policyIteration( self, gamma=0.7 ):
        '''
        Performs policy iteration starting from the policy of the predator.
        '''
        now = time.time()
        
        # Initialization
        stable = False
                
        while not stable:
            # 1. Policy evaluation
            V = self.policyEvaluation( gamma )
            
            # 2. Policy Improvement
            stable = self.policyImprovement( V, gamma )

        print 'Time taken (seconds): ', time.time() - now
        return V

    def policyImprovement( self, V, gamma=0.7 ):
        '''
        Performs policy improvement, given the value function V.        
        '''
        
        updated = 0
        stable = True
        
        for s in self.S:
            # Retrieve action according to policy
            policy_action = self.Predator.getAction( s )
            
            best_action = None
            best_value = None
            
            # Check all possible actions
            for a in self.Predator.actions:                
                current_value = 0
                
                # Calculate next states and their probabilities
                P = self.nextStates( s, a )
                
                for s_prime in P:
                    current_value += P[s_prime] * ( self.reward( s, a, s_prime ) + gamma * V[s_prime] )
                    
                if current_value > best_value:
                    best_value = current_value                    
                    best_action = a                    

            # Update the policy
            self.Predator.updatePolicy( s, best_action )
            
            # Check policy stability
            if best_action != policy_action:
                updated += 1
                stable = False
            
        print 'Updated', updated, 'actions'
        return stable
        
    def reset(self):
        '''
        Reset the position of the prey and predator in this environment.        
        '''
        self.Prey.location = (5,5)
        self.Predator.location = (0,0)
        