# Assignment:   MultiAgent Planning&Learning
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
import random

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
        self.numberOfPredators = numberOfPredators
        self.S,self.terminal_states = self.getStates()
        
        self.Prey = Prey( self, preyLocation )
        self.PredatorLocations = [(0,0), (10,0), (0,10), (10,10)]

        self.Predators = [Predator(self, self.predatorLocations[i]) \
                          for i in range(self.numberOfPredators)]        

           
    def environmentStep(self):
        '''
        s_prime = environmentStep()
        
        Perform one step (for the prey and each predator), given the current 
        state s.
        '''
        
    def qLearning( self, 
           episodes=1000, 
           alpha=0.1, 
           gamma=0.1, 
           epsilon=0.1, 
           optimistic_init=15,
           verbose=False):
        '''
        Q, return_list <- qLearning(episodes, 
                                    alpha, 
                                    gamma, 
                                    epsilon,
                                    optimistic_init)
        
        Implementation of Q-learning given the learning rate alpha, discount
        factor gamma, epsilon for epsilon-greedy policy or temperature tau for
        softmax action selection. Integer optimistic_init is used 
        to initialize Q, and should be larger than zero.

        Note that if epsilongreedy == False, epsilon will be used as the 
        temperature tau.
        
        Returns the values of Q as a 2-deep dict (Q[s][a]) and a list
        containing performance measures of the agent (number of steps).
        '''
        
        now = time.time()            
        # For a number of episodes
        for n in xrange(1,episodes+1):
            
            if verbose and n % 50 == 0:
                print 'Episode {0}, time taken: {1}.'.format(n, time.time()-now)
                now = time.time()
                
            # Initialize the beginstate s semi-randomly
            s = [(0,0)] + [(random.randint(-5,5), random.randint(-5,5)) \
                           for i in range(self.numberOfPredators)]

            game_over = False
            step_number = 0           
            
            # Run through one episode
            while not game_over:      
                step_number += 1
        
                # All agents take one QLearning step simultaneously, but we
                # calculate the state that results from the prey's new position
                actions = list()              
                for Agent in self.Agents:                    
                    # Find a sample action (epsilon-greedy) given the state
                    a = self.Agent.deriveAction(s)
                    actions.append(a)
                    
                    # Perform that action
                    Agent.performAction(Agent.Q, s, Agent.epsilon)
                    
                # Derive the new state from updated agent locations
                s_prime = self.deriveState([Agent.location for Agent in \
                                            self.Agents])                                
                
                # This results in reward
                r, game_over = self.reward(s_prime)
                
                # Update Q for each agent
                for i in xrange(len(self.Agents)):
                    self.Agents[i].QLearning.updateQ( s, 
                                                      actions[i], 
                                                      s_prime, 
                                                      r )
                # Update the state
                s = s_prime
           
    def getStates(self):
        '''
        Gets the entire statespace in two sets, the first containing the non-
        terminal states and the second containing terminal states.
        '''
        S = set()
        terminal_states = set()
    
        for i in xrange( -(self.width/2), self.width/2+1 ):
            for j in xrange( -(self.height/2), self.height/2+1 ):
                s = list() 
                for p in xrange(self.numberOfPredators):
                    s.append( (i,j) )
                # If absorbing (reached predator/two predators at one spot)
                if (0,0) in s or len(s) != len(set(s)):
                    terminal_states.add( s )
                else:
                    S.add( s )
                    
        return S, terminal_states    
    
    def reward( self, s ):
        '''
        r, game_over <- reward(s)

        Returns the reward for a given state containing location of 
        the predators and prey. Return is the reward of the predator(s), as 
        this is a zero-sum-game, the reward of the predator is simply the 
        negated reward of the prey. Boolean game_over indicates if the state 
        is absorbing.
        '''
        # Prioritize confusion of predators            
        if len(s) != len(set(s)):
            return -10, True
        elif (0,0) in s:
            return 10, True
        else:
            return 0, False

    def reset(self):
        '''
        Reset the position of the prey and predator in this environment.        
        '''
        self.Prey.location = (5,5)
        self.Predators = [Predator(self, self.predatorLocations[i]) \
                          for i in range(self.numberOfPredators)]        
    