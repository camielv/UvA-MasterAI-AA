# Assignment:   MultiAgent Planning&Learning
# Course:       Autonomous Agents 2012-2013
# Education:    Master Artificial Intelligence
# By:           Steven Laan
#               Auke Wiggers
#               Camiel Verschoor
#
# File:         environment.py
# Description:  Base class of the environment.
from TeamPredator import TeamPredator
from TeamPrey import TeamPrey
try:
    import gurobipy as grb
except:
    print 'No Gurobi = no minimax-Q-learning'
    
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
        
        self.TeamPrey = TeamPrey( self, preyLocation )
        self.PredatorLocations = [(0,0), (10,0), (0,10), (10,10)]
        self.TeamPredator = TeamPredator(self, self.PredatorLocations)
        
    def minimaxQLearning( self ):

        done = False
        self.resetAgents()
        s = self.gameState()

        while not done:
            # In state s take action a and opponent action o to get reward r and
            # state s_prime
            
            # Find the optimal action, epsilon greedy
            a_teamPred = self.TeamPredator.getJointActionEpsilonGreedy( s )
            a_teamPrey = self.TeamPrey.getActionEpsilonGreedy( s )
            
            # Each team performs the found action
            self.TeamPredator.performJointAction( s, a_teamPred )
            self.TeamPrey.performAction( s, a_teamPrey )
            
            s_prime = self.gameState()
            reward, game_over = self.reward(s_prime)
            
            # update Q : State , own action, opponent action
            self.TeamPredator.updateQ(s, a_teamPred, a_teamPrey, s_prime, reward)
            self.TeamPrey.updateQ(s, a_teamPrey, a_teamPred, s_prime, reward)
            
            s = s_prime
            
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

        for i in xrange( self.numberOfPredators ):
            predator_x, predator_y = locations[i+1]
            x = ( ( 5 + prey_x - predator_x ) % ( self.width ) ) - 5
            y = ( ( 5 + prey_y - predator_y ) % ( self.height ) ) - 5
            state.append( (x, y) )

        return tuple(state)

    def gameState( self ):
        '''
        state <- deriveState( gameState ) 
        
        Derives the gamestate based on agents location
        '''
        state = list()
        prey_x, prey_y = self.TeamPrey.Prey.location
        for Predator in self.TeamPredator.Predators:
            predator_x, predator_y = Predator.location
            x = ( ( 5 + prey_x - predator_x ) % ( self.width ) ) - 5
            y = ( ( 5 + prey_y - predator_y ) % ( self.height ) ) - 5
            state.append( (x, y) )

        return tuple(state)

    def resetAgents(self):
        '''
        Reset the position of the prey and predator in this environment.        
        '''
        self.TeamPrey.Prey.location = (5,5)
        for Predator in self.TeamPredator.Predators:
            Predator.location = (random.randint(-5,5), random.randint(-5,5))        
    
    def simulateEnvironment(self):
        ''''
        simulateEnvironment(reset=False)

        Simulate the environment for one step. Location of each agent is 
        updated. Returns a list of agent locations. 
        '''                
        s = self.gameState()
        
        for Agent in self.Agents:
            # Get an action based on Q
            a = Agent.getActionEpsilonGreedy(s)
            # Update location
            Agent.performAction(a)
