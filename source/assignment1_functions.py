# Autonomous Agents - 2012/2013
# Team SuperAuke
#
# valueIteration.py
# Base class for the prey

import copy

def policyEvaluation():
    
    policy = {(0,0) : 0.2,
              (1,0) : 0.2,
              (0,1) : 0.2, 
              (-1,0): 0.2,
              (0,-1): 0.2 }
              
    discount = 0.8

    state_dict = dict()

    for i in range(11):
        for j in range(11):
            for k in range(11):
                for m in range(11):
                    state_dict[(i,j,k,m)] = 0
           
                        
    delta = 0.2   
    theta = 0.01    
    new_state_dict = dict()    
    
    while delta > theta:
        delta = 0
        for i in range(11):
            for j in range(11):
                for k in range(11):
                    for m in range(11):
                        # state representation
                        s = (i,j,k,m)
                        new_state_dict[s] = 0
                        
                        v = state_dict[s]                        
                        
                        V = 0
                        # policy is dict, where a is the key
                        # and the values are probabilities of the move a
                        for a in policy:
                            next_state = nextState( s, a )
                            V += policy[a] *( reward( next_state ) + discount * state_dict[next_state] )
                        new_state_dict[s] = V
                        
                        delta = max(delta, abs(v-V))
        print new_state_dict[(5,5,5,5)]
        print delta
        
                        
        state_dict = copy.deepcopy(new_state_dict)
    return state_dict

def reward( state ):
    if (state[0],state[1]) == (state[2], state[3]):
        return 10
    return 0

def nextState( state, action ):

    old_x, old_y = (state[0], state[1])
    # determine the new location based on environment borders
    new_x = (old_x + action[0]) % 11
    new_y = (old_y + action[1]) % 11
    
    return (new_x, new_y, state[2],state[3])  
        

"""def valueIteration():
    V = dict()
    V[s] = 0
    
    delta = 0
    for s in stateSpace:
        v = V[s]
        # new value is the max of
        # sum 
        V[s] = max_action
        """