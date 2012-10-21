from Predator import Predator
from TeamQLearning import TeamQLearning
from itertools import izip, product
import gurobipy as grb
import random

argmax = lambda d: max( izip( d.itervalues(), d.iterkeys() ) )[1]    

class TeamPredator():

    def __init__(self, Environment, myLocation):
        self.Environment = Environment
        # Initialize Q
        alpha = 0.3
        gamma = 0.7
        epsilon = 0.1
    
        # Initialize the predators in this team
        self.Predator = Predator( Environment, myLocation )             
        self.actions = self.Predator.actions
        self.TeamQLearning = TeamQLearning(self, alpha, gamma, epsilon)
        
            
    def updateQ(self, s, a, o, s_prime, r):
        '''
        Update this teams Q and V.
        '''
        O = self.actions
        A = self.actions
        
        # Use linear programming to obtain optimal policy for this state
        try:
            # Create a new model
            m = grb.Model("MultiAgentMinimax")
            m.setParam("OutputFlag",0)
            
            # Create variables
            pi = dict()
            for a in A:
                pi[a] = m.addVar( 0.0, 1.0, vtype = grb.GRB.CONTINUOUS, name = str(a) )
        
            # Integrate new variables
            m.update()            
        
            # Set objective
            m.setObjective( grb.LinExpr( [ ( self.TeamQLearning.Q[s][(a,o)], pi[a] ) for o in O for a in A ] ), grb.GRB.MAXIMIZE)
        
            # Add constraint: Sum_a pi(a) = 1
            expr = grb.quicksum( m.getVars() )
            m.addConstr( expr == 1, "Total probability" )
        
            # Add more constraints
            for o in O:
                expr = grb.LinExpr( [ (self.TeamQLearning.Q[s][(a,o)], pi[a]) for a in self.actions ] )
                m.addConstr( expr >= 0 )
            
            m.optimize()
            
            for a in A:
                self.TeamQLearning.policy[s][a] = pi[a].x
        
        except grb.GurobiError:
            print 'Error reported'
            
        # Update Q and V
        self.TeamQLearning.updateQ(s, a, o, s_prime, r)

    def getJointActionEpsilonGreedy(self, s):
        # Find the (joint) action that maximizes Q[(s, a)]                
        prob_actions = dict()        
        uniform_epsilon = self.TeamQLearning.epsilon / (len(self.actions))
        
        for possible_a in self.actions:
            # Set probabilities of all actions uniformly
            prob_actions[possible_a] = uniform_epsilon
            
        best_a = argmax( self.TeamQLearning.policy[s] )
        prob_actions[best_a] += 1 - self.TeamQLearning.epsilon
                    
        # For every action, check if the cumulative probability exceeds a 
        # random number. 
        random_number = random.random()
        cumulative_prob = 0.0
        
        for a in self.actions:
            cumulative_prob += prob_actions[a]
            if cumulative_prob >= random_number:                
                return a
                
    def performAction(self, a):
        self.Predator.performAction(a)
        
    def performJointAction(self, a):
        for n in xrange(self.Environment.numberOfPredators):
            self.Predators[n].performAction(a)
             
    def permutations(self, iterable, r=None):	  	
        '''  	
        iterator <- permutations(iterable, r)        
  	
        Finds permutations of iterable of length r, with duplicate entries.  	
        ''' 	
        pool = tuple(iterable)	  	
        n = len(pool)	
        r = n if r is None else r
  	
        for indices in product(range(n), repeat=r):  	
            if len(indices) == r:
                yield tuple(pool[i] for i in indices)
                        
    
