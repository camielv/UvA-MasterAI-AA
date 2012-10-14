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

import itertools
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
                  numberOfPredators=1  ):
                      
        assert numberOfPredators > 0
        assert numberOfPredators < 5
        assert type(numberOfPredators) == int        
        
        self.width  = width
        self.height = height
        self.numberOfPredators = numberOfPredators
        print "Determining the statespace..."
        self.S,self.terminal_states = self.getStates()
        print "Size of the statespace: {} states.".format(len(self.S) + \
                                                          len(self.terminal_states))
        print "Adding agents to the environment.."
        self.Prey = Prey( self, preyLocation )
        self.PredatorLocations = [(0,0), (10,0), (0,10), (10,10)]
        self.Predators = [Predator(self, self.PredatorLocations[i]) \
                          for i in range(self.numberOfPredators)]        
        self.Agents = [self.Prey] + self.Predators
        print 'Environment initialized.'
           
    def environmentStep(self):
        '''
        s_prime = environmentStep()
        
        Perform one step (for the prey and each predator), given the current 
        state s.
        '''
        
    def qLearning( self, 
           episodes=1000, 
           optimistic_init=15,
           verbose=False,
           return_num_of_steps=True):
        '''
        Q, return_list <- qLearning(episodes, 
                                    optimistic_init,
                                    verbose)
        
        Implementation of Q-learning. Integer optimistic_init is used 
        to initialize Q, and should be larger than zero.
        '''
        print "Performing independent Q-Learning for {0} predator(s) and \
               one prey.".format(self.numberOfPredators)        
        
        now = time.time()            
        # Keep track of number of steps/return (for performance measures)
        return_list = list()
        # For a number of episodes
        for n in xrange(1,episodes+1):
            
            if verbose and n % 1000 == 0:
                print 'Episode {0}, time taken: {1}.'.format(n, time.time()-now)
                now = time.time()
                
            # Initialize the beginstate s semi-randomly
            self.reset()                
            s = self.deriveState([Agent.location for Agent in self.Agents])
            game_over = False
            step_number = 0           
            
            
            # Run through one episode
            while not game_over:      
                step_number += 1
                
                #print '\nCurrent', [Agent.location for Agent in \
                #                            self.Agents]                
                
                # All agents take one QLearning step simultaneously, but we
                # calculate the state that results from the prey's new position
                actions = list()              
                for Agent in self.Agents:                    
                    # Find a sample action (epsilon-greedy) given the state
                    a = Agent.getActionEpsilonGreedy(s)
                    
                    # Perform that action
                    Agent.performAction(a)
                    # And save it                    
                    actions.append(a)
                
                # Derive the new state from updated agent locations
                s_prime = self.deriveState([Agent.location for Agent in \
                                            self.Agents]) 
                
                #print 'Next', [Agent.location for Agent in \
                #                            self.Agents]                
                #print 'Moved from ', s, 'to', s_prime
                
                # This results in reward
                r, game_over = self.reward(s_prime)
                # Update Q for each agent
                for i in xrange(len(self.Agents)):
                    self.Agents[i].updateQ( s, 
                                            actions[i], 
                                            s_prime, 
                                            r )
                # Update the state
                s = s_prime
            
            if return_num_of_steps:       
                return_list.append(step_number)
            else:
                total_return = list()
                # Only the prey and one predator matter, since return is the
                # same for every predator 
                for Agent in self.Agents[0:2]:
                    total_return.append( r * Agent.QLearning.alpha ** step_number)
                # Negate prey reward, as reward function is from predator POV
                total_return[0] = -total_return[0]
                
                return_list.append(total_return)
           
        Q_agents = list()
        for Agent in self.Agents:
            Q_agents.append(Agent.QLearning.Q)
            
        return Q_agents, return_list
          
    def getStates(self):
        '''
        S, terminal_states <- getStates()        
        
        Gets the entire statespace in two sets, the first containing the non-
        terminal states and the second containing terminal states.
        '''
        S = set()
        terminal_states = set()
        
        # Get all possible positions        
        allLocs = list()
        for i in xrange(-5, 6):
            for j in xrange(-5,6):
                allLocs.append( (i,j) )

        # Get combinations of P positions
        for s in self.permutations(allLocs, self.numberOfPredators):
            # If absorbing (reached predator/two predators at one spot)
            if (0,0) in s or len(s) != len(set(s)):
                terminal_states.add( tuple(s) )
            else:
                S.add( tuple(s) )
        return S, terminal_states    
    
    
    def permutations(self, iterable, r=None):
        '''
        iterator <- permutations(iterable, r)        
        
        Finds permutations of iterable of length r, with duplicate entries.
        '''
        pool = tuple(iterable)
        n = len(pool)
        r = n if r is None else r
        for indices in itertools.product(range(n), repeat=r):
            if len(indices) == r:
                yield tuple(pool[i] for i in indices)
            
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
 
    def deriveState( self, locations ):
        '''
        state <- deriveState( locations )        
        
        Derive the state based on the locations of the prey and the predators.
        '''
        state = list()
        prey_x, prey_y = locations[0]

        for i in range( self.numberOfPredators ):
            predator_x, predator_y = locations[i+1]
            x = ( ( 5 + prey_x - predator_x ) % ( self.width ) ) - 5
            y = ( ( 5 + prey_y - predator_y ) % ( self.height ) ) - 5
            state.append( (x, y) )

        return tuple(state)

    def reset(self):
        '''
        Reset the position of the prey and predator in this environment.        
        '''
        self.Prey.location = (5,5)
        for Predator in self.Predators:
            Predator.location = (random.randint(0,10), random.randint(0,10))