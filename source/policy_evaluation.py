# Autonomous Agents - 2012/2013
# Team SuperAuke
#
# valueIteration.py
# Base class for the prey

import copy

def policyEvaluation():
    
    # Define the set of actions
    actions = set( [ (0,0),(1,0), (0,1), (-1,0), (0,-1) ] )
              
    # Define the discount
    discount = 0.8

    # Define the set of all states
    S = set( [ (i,j,k,m) for i in range(11) for j in range(11) for k in range(11) for m in range(11) ] )

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
    
    # Policy iteration
    while delta > theta:
        delta = 0
        
        for s in S:
            new_V[s] = 0
            v = V[s]                        
            
            for a in actions:
                # Calculate all next states and their probabilities
                next_states, P = nextStates( s, a )
                
                for next_state in next_states:
                    new_V[s] += policy([s,a)] * P[next_state] * ( reward( next_state ) + discount * V[next_state] )
            
            # Compute the error
            delta = max( delta, abs( v - new_V[s] ) )

        # Store the new values
        V = copy.deepcopy(new_V)
        
    return V

def reward( state ):
    
    if (state[0],state[1]) == (state[2], state[3]):
        return 10
    return 0

def nextStates( state, action, prey ):
    '''
    Returns a tuple containing a list of all possible next states and a
    dictionary containing the transition probabilities of those next states.
    '''
    old_predator_x, old_predator_y = (state[0], state[1])
    
    # determine the new location based on environment borders
    new_predator_x = (old_predator_x + action[0]) % self.getWidth()
    new_predator_y = (old_predator_y + action[1]) % self.getHeight()
   
    moves = prey.getPossibleMoves(  self.getWidth(), self.getHeight(), (new_predator_x, new_predator_y, state[2], state[3]) )
    
    return [(new_x, new_y, state[2],state[3])], { (new_x, new_y, state[2],state[3]) : 1}
        
