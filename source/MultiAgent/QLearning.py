# Assignment:   MultiAgent Planning/Learning
# Course:       Autonomous Agents 2012-2013
# Education:    Master Artificial Intelligence
# By:           Steven Laan
#               Auke Wiggers
#               Camiel Verschoor
#
# File:         QLearning.py
# Description:  Implementation of Q-learning

import time    
import random
from itertools import izip
from tables import *

'''
Pytables use instructions
 1. Maak een h5 file aan
 2. Maak een group aan aan de hand van die h5file
 3. Maak een tabel zoals je een klasse met fields aan zou maken
 4. Maak de tabel daadwerkelijk aan mbv de h5file
 5. Maak een rowobject aan
 6. Vul de row
 7. Append de row
 8. Repeat 5-7
 9. Flush de tabel (wat het ook is , het zorgt ervoor dat I/O niet meer mogelijk is:D)
10. Maak een readobject aan mbv de h5file
11. Lees de tabel uit als een iterable    
'''

class Q1(IsDescription):
    x_pos1 = UInt16Col()
    y_pos1 = UInt16Col()
    x_action = UInt16Col()
    y_action = UInt16Col() 
    q_val = UInt16Col()
class Q2(IsDescription):
    x_pos1 = UInt16Col()
    y_pos1 = UInt16Col()
    x_pos2 = UInt16Col()
    y_pos2 = UInt16Col()
    x_action = UInt16Col()
    y_action = UInt16Col()  
    q_val = UInt16Col()
class Q3(IsDescription):
    x_pos1 = UInt16Col()
    y_pos1 = UInt16Col()
    x_pos2 = UInt16Col()
    y_pos2 = UInt16Col()
    x_pos3 = UInt16Col()
    y_pos3 = UInt16Col()
    x_action = UInt16Col()
    y_action = UInt16Col()  
    q_val = UInt16Col()
class Q4(IsDescription):
    x_pos1 = UInt16Col()
    y_pos1 = UInt16Col()
    x_pos2 = UInt16Col()
    y_pos2 = UInt16Col()
    x_pos3 = UInt16Col()
    y_pos3 = UInt16Col()
    x_pos4 = UInt16Col()
    y_pos4 = UInt16Col()
    x_action = UInt16Col()
    y_action = UInt16Col() 
    q_val = UInt16Col()

QTables = {1:Q1, 2:Q2, 3:Q3, 4:Q4}

argmax = lambda d: max( izip( d.itervalues(), d.iterkeys() ) )[1]    
    
class QLearning():
    '''    
    Implementation of functions related to Q-learning.    
    '''
    
    def __init__(self, 
                 Agent, 
                 alpha, 
                 gamma, 
                 epsilon, 
                 optimistic_value=5):
        '''
        Fill all values of Q based on a given optimistic value.
        '''

        # Set the agent for this QLearning session
        self.Agent = Agent
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon

        self.numberOfPredators = self.Agent.Environment.numberOfPredators 

        # Create storage for Q-values
        self.h5file = openFile("qvalues {0}.h5".format(Agent.agent_ID), 
                          mode="w", 
                          title="qvalues")
        self.group  = h5file.createGroup("/", "q_vals", "Q-Learning values")
        self.qTable = h5file.createTable(group, 
                                         "readout", 
                                         QTables[self.Agent.Environment.numberOfPredators], 
                                         "")

        # Value of any nonterminal state is the optimistic value
        qRow = qTable.row
        qRow['q_val'] = optimistic_value
        for s in self.Agent.Environment.S:
            # split the state into multiple parts
            for p in xrange(self.numberOfPredators):
                x_pos, y_pos = s[p]
                qRow['x_pos{0}'.format(p)] = x_pos
                qRow['y_pos{0}'.format(p)] = y_pos
            # store for every state/action combination
            for (a_x,a_y) in self.Agent.actions:
                qRow['x_action'] = x_pos
                qRow['y_action'] = y_pos
                
                qRow.append()    

        # Value of absorbing state(s) is 0
        qRow['q_val'] = 0
        for s in self.Agent.Environment.terminal_states:
            # split the state into multiple parts
            for p in xrange(self.numberOfPredators):
                x_pos, y_pos = s[p]
                qRow['x_pos{0}'.format(p)] = x_pos
                qRow['y_pos{0}'.format(p)] = y_pos
            # store for every state/action combination
            for (a_x,a_y) in self.Agent.actions:
                qRow['x_action'] = x_pos
                qRow['y_action'] = y_pos
                
                qRow.append()    
        
        qTable.flush()

        self.readQTable = self.h5file.root.q_vals.readout   


    def updateQ(self, s, a, s_prime, r):
        '''
        Perform one step for this agent for a given state s. Action, resulting
        state s_prime, and observed reward r are also given.         
        '''

        if self.numberOfPredators == 1:
            qVals_s_prime = [qRow['q_val'] for qRow in readQTable.where
                                ("""
                                    qRow['x_pos1'] == s[0][0] & qRow['y_pos1'] == s[0][1]          
                                """) 
                            ]
            qVal_s = qVals_s_prime = [qRow['q_val'] for qRow in readQTable.where
                        ("""
                             qRow['x_pos1'] == s[0][0] & qRow['y_pos1'] == s[0][1] &
                             qRow['x_action'] == a[0] & qRow['y_action'] == a[1]
                         """) 
                                     ]
                                     
        print qVals_s_prime
        print qVal_s
            
        # Determine which action maximizes Q(s,a)
        max_Q = self.Q[s_prime][argmax( self.Q[s_prime] )]
        
        # Update Q
        self.Q[s][a] += self.alpha * (r + self.gamma * max_Q - self.Q[s][a])
        