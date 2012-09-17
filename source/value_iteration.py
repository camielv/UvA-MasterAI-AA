# -*- coding: utf-8 -*-
"""
Created on Sat Sep 15 15:13:54 2012

@author: Steven
"""

size = 11
discount = 0.7

theta = 0.0001
delta = 1

S = set()
V = dict()
new_V = dict()
actions = set( [ (0,0), (1,0), (0,1), (-1,0), (0,-1) ] )
terminal_states = set()

def performMove( state, action, prey ):  
    if prey:
        x,y = state[0],state[1]
    else:
        x,y = state[2],state[3]
    
    new_x = (x + action[0]) % size
    new_y = (y + action[1]) % size
    
    if prey:
        return ( new_x, new_y, state[2], state[3] )
    else:
        return ( state[0], state[1], new_x, new_y )
        
def preyMoves( state ):
    next_states = dict()
    
    if state in terminal_states:
        next_states[state] = 1
        return next_states
        
    for a in actions:
        new_state = performMove( state, a, True )
        if not new_state in terminal_states:
            next_states[new_state] = 1
    
    p_move = 0.2 / ( len( next_states ) - 1 )   
    #next_states[state] = 0.8
    
    for s in next_states:
        if s == state:
            next_states[s] = 0.8
        else:
            next_states[s] = p_move
            
    return next_states

def nextStates( state, action ):
    new_state = performMove( state, action, False )
    return preyMoves( new_state )
    #new_states = preyMoves( state )
    #next_states = dict()    
    #for new_state in new_states:
    #    next_states[ performMove( new_state, action, False ) ] = new_states[new_state]
    #return next_states
    
def reward( state ):        
    if (state[0],state[1]) == (state[2], state[3]):
        return 10
    return 0

# Initialize V and S
for i in xrange( size ):
    for j in xrange( size ):
        for k in xrange( size ):
            for m in xrange( size ):
                s = (i,j,k,m)          
                V[s] = 0                
                if i == k and j == m:
                    terminal_states.add( s )
                else:
                    S.add( s )
                
# Define the policy (currently random: 5 actions per state, each prob(a) = 0.2)
policy = dict()
for s in S:
    for a in actions:
        policy[(s,a)] = 0.2

# Define delta and theta
delta = 0.2   
theta = 0.001    

step = False
view = False
# Policy evaluation
while delta > theta:
    delta = 0
        
    for s in S:
        new_V[s] = 0                      
        
        best_value = None
        best_action = None
        
        for a in actions:
            current_value = 0
            policy[ (s, a ) ] = 0
            
            # Calculate all next states and their probabilities
            P = nextStates( s, a )
            
            for next_state in P:
                current_value +=  P[next_state] * ( reward( next_state ) + discount * V[next_state] )
        
            if current_value > best_value:
                best_value = current_value
                best_action = a
                
        policy[ ( s, best_action ) ] = 1.0            
        new_V[s] = best_value
        
        # Compute the error
        delta = max( delta, abs( V[s] - new_V[s] ) )

    # Store the new values
    for s in S:
        V[s] = new_V[s]