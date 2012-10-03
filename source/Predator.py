# Assignment:   Single Agent Learning
# Course:       Autonomous Agents 2012-2013
# Education:    Master Artificial Intelligence
# By:           Steven Laan
#               Auke Wiggers
#               Camiel Verschoor
#
# File:         Predator.py
# Description:  Predator is a class containing properties of the agent, such as
#               the policy, as well as functions that enable movement.

import random
from itertools import izip
import time
from math import exp

argmax = lambda d: max( izip( d.itervalues(), d.iterkeys() ) )[1]

class Predator():
    '''
    Creates an agent which contains a policy. Input are an environment object
    and the location of the agent, which is (0,0) by default.    
    '''
    
    ACTION_UP    = (-1, 0)
    ACTION_DOWN  = ( 1, 0)
    ACTION_RIGHT = ( 0, 1)
    ACTION_LEFT  = ( 0,-1)
    ACTION_STAY  = ( 0, 0)   
    
    actions = set([ACTION_UP, ACTION_DOWN, ACTION_RIGHT, ACTION_LEFT, ACTION_STAY])
    policy = dict()
    
    location = None
    
    def __init__( self, environment, location=(0,0) ):
        self.location = location
        self.Environment = environment
        # For every non-terminal state in the statespace, determine the 
        # possible actions and their probabilities.
        for s in self.Environment.S:
            for a in self.actions:
                self.policy[(s,a)] = 0.2
                    
    def simulateAction( self, s, reduced ):
        '''
        Perform an action based on the policy, given the s
        '''
        
        # Determine which function should be used based on a boolean 'reduced'.
        # If the boolean is true, the reduced sspace will be used.
        if not reduced:
            performAction = self.performAction
        else:
            performAction = self.performActionReduced
        
        a = self.getAction( s ) 
        
        s_prime = performAction( s, a )

        # If the 2D staterepresentation is used instead of the 4D one
        if reduced:          
            # Use a different method to update the state
            new_x = self.location[0] - (s[0] - s_prime[0])
            new_y = self.location[1] - (s[1] - s_prime[1])
            
            new_x = new_x % self.Environment.width
            new_y = new_y % self.Environment.height
            self.location = (new_x, new_y)
        else:
            self.location = (s_prime[0], s_prime[1])
        return s_prime

    def getAction( self, s ):
        '''
        Get an action given the current state, using the policy. 
        '''
        random_number = random.random()

        cumulative_prob = 0.0
        
        # For every action, check if the cumulative probability exceeds a 
        # random number. 
        for a in self.actions:
            cumulative_prob += self.policy[(s,a)]
            if cumulative_prob >= random_number:                
                return a

    def performAction( self, s, a ):
        ''' 
        Update the location based on a given action, regardless of policy. 
        '''
        x,y = s[0],s[1]
        
        new_x = (x + a[0]) % self.Environment.width
        new_y = (y + a[1]) % self.Environment.height
       
        return ( new_x, new_y, s[2], s[3] )

    def performActionReduced( self, s, a ):
        ''' 
        Update the location based on a given action. Reduced s version. 
        '''
        d_x, d_y  = a
        old_x, old_y = s

        max_x = self.Environment.width
        max_y = self.Environment.height

        # There are, for this environment, 3 cases per dimension:
        if old_x < 0:
            # If the predator is not on the same y-axis as the prey, a move
            # in horizontal direction will be either towards or away from 
            # the prey, or a standstill.
            new_x = ((old_x + 5 - a[0]) % max_x)-5
        elif old_x > 0:
            new_x = ((old_x + 5 - a[0]) % max_x)-5
        elif old_x == 0:
            # If it is on the same y-axis, any action in horizontal direction 
            # will be a move away from the prey.
            new_x = -a[0]
            
        # The same principle applies to moves in vertical direction
        if old_y < 0:   
            new_y = ((old_y + 5 - a[1]) % max_y)-5
        elif old_y > 0:
            new_y = ((old_y + 5 - a[1]) % max_y)-5
        elif old_y == 0:
            new_y = -a[1]

        return (new_x, new_y)

    def updatePolicy( self, s, best_a ):
        '''
        Given a state and the best action, this function sets the predators 
        policy so that in state s, the probability of taking action best_a is
        1.0 and probabilities of taking any other actions are (of course) 0. 
        '''
        # Set probabilities of all actions to 0
        for a in self.actions:
            self.policy[(s,a)] = 0.0
            
        # Give the new action for this state a probability of 1
        self.policy[(s,best_a)] = 1.0
       
    def sarsa( self, episodes=1000, alpha=0.1, gamma=0.1, epsilon=0.1 ):
        '''
        Implementation of Sarsa given the learning rate alpha, discount
        factor gamma, epislon for epsilon-greedy policy, and the number of
        episodes.
        '''
        # Initialize Q
        Q = self.init_Q

        for n in xrange( episodes ):
            if n%100 == 0:
                print "Episodes: ", n

            # Current state
            s = (random.randint(-5,5), random.randint(-5,5))
            prey_caught = False

            # Determine which action maximizes Q(s,a)
            a = self.deriveActionSarsa(Q, s, epsilon)

            while not prey_caught:
                # Take action a, observe r and s_prime
                r, s_prime, prey_caught = self.takeAction(s, a)
                
                # Determine which next action maximizes Q(s',a')
                a_prime = self.deriveActionSarsa(Q, s, epsilon)

                # Update Q
                Q[s][a] = Q[s][a] + alpha * (r + gamma * Q[s_prime][a_prime] - Q[s][a])

                # Update state and action
                s = s_prime
                a = a_prime
        return Q

    def deriveActionSarsa( self, Q, s, epsilon ):
        '''
        Find the action that maximizes Q[(s, a)]
        '''
        prob_actions = dict()        
        uniform_epsilon = epsilon / len(self.actions)
        
        for possible_a in self.actions:
            # Set probabilities of all actions uniformly
            prob_actions[possible_a] = uniform_epsilon
        
        best_a = argmax( Q[s] )
        
        # Update policy of predator
        self.updatePolicyEpsilonGreedy( s, best_a, epsilon )

        # Give the best action for this state a probability of 1
        prob_actions[best_a] += 1 - epsilon

        # For every action, check if the cumulative probability exceeds a 
        # random number. 
        random_number = random.random()
        cumulative_prob = 0.0
        
        for a in self.actions:
            cumulative_prob += prob_actions[(s,a)]
            if cumulative_prob >= random_number:                
                return a

    def init_Q(self, optimistic_value=15):    
        '''
        Fill all values of Q based on a given optimistic value.
        '''
        Q = dict()
        # Value of any nonterminal state is the optimistic value
        for s in self.Environment.S:
            Q[s] = dict()            
            for a in self.actions:
                Q[s][a] = optimistic_value

        # Value of absorbing state(s) is 0
        for s in self.Environment.terminal_states:
            Q[s] = dict()            
            for a in self.actions:
                Q[s][a] = 0        

        return Q

    def qLearning( self, 
                   episodes=1000, 
                   alpha=0.1, 
                   gamma=0.1, 
                   epsilon_or_tau=0.1, 
                   epsilongreedy=True,
                   optimistic_value=15 ):
        '''
        Q, return_list <- qLearning(episodes, 
                                    alpha, 
                                    gamma, 
                                    epsilon_or_tau, 
                                    epsilongreedy,
                                    optimistic_value)
        
        Implementation of Q-learning given the learning rate alpha, discount
        factor gamma, epsilon for epsilon-greedy policy or temperature tau for
        softmax action selection. Boolean epsilongreedy determines whether 
        softmax or epsilon-greedy is used. Integer optimistic_value is used 
        to initialize Q, and should be larger than zero.
        
        Returns the values of Q as a 2-deep dict (Q[s][a]) and a list
        containing performance measures of the agent (number of steps).
        '''

        # Use either softmax or epsilon greedy action selection
        if epsilongreedy:
            print 'Using epsilon-greedy action selection.'
            findAction = self.deriveAction
        else:
            print 'Using softmax action selection.'
            findAction = self.deriveActionSoftmax

        # Initialize Q            
        Q = self.init_Q( optimistic_value )    
        
        return_list = list()
            
        now = time.time()            
        
        # For a number of episodes
        for n in xrange(1,episodes+1):
            
            if n % 100 == 0:
                print 'Episode {0}, time taken: {1}.'.format(n, time.time()-now)
                now = time.time()
                
            # Initialize s
            s = (random.randint(-5,5), random.randint(-5,5))

            prey_caught = False
            step_number = 0           
            
            # Run through one episode
            while not prey_caught:      
                step_number += 1
               
                # Choose action a from state s using policy derived from Q 
                # (epsilon greedy or softmax, based on arguments tau and 
                # epsilon)
                a = findAction(Q, s, epsilon_or_tau)
                
                # Take action a, observe r, s_prime
                r, s_prime, prey_caught = self.takeAction(s, a)                
                
                # Determine which action maximizes Q(s,a)
                max_Q = Q[s_prime][argmax( Q[s_prime] )]
                
                # Update Q
                Q[s][a] = Q[s][a] + alpha * (r + gamma * max_Q - Q[s][a])
               
                # Update the state        
                s = s_prime
                
            # Finds both the average number of steps and return for X
            # simulations using a given Q.
            average_steps = self.simulate_X_times_using_Q(100, 
                                                          Q, 
                                                          epsilon_or_tau, 
                                                          epsilongreedy)
        
            return_list.append(average_steps) 

        # Return the found Qvalues and simulation data
        return Q, return_list
            
    def simulate_X_times_using_Q( self, X, Q, epsilon_or_tau, epsilongreedy):
        '''
        Simulate the environment containing prey and predator a number of X
        times, using a state-action value function Q, for an epsilon greedy
        policy derived from Q. Returns an average number of steps needed to 
        catch the prey.        
        '''

        # This construction enables the use of softmax or epsilongreedy        
        if epsilongreedy:
            findAction = self.deriveAction
        else:
            findAction = self.deriveActionSoftmax
        
        # Keep track of the total number of steps
        total_step_numbers = 0
        
        for i in range(X):
            # Initialize variables which will keep track of the current run i
            step_number = 0
            prey_caught = False
            
            # Initialize s
            s = (random.randint(-5,5), random.randint(-5,5))
 
            while not prey_caught:      
                step_number += 1
                # Choose a from s using policy derived from Q (epsilon greedy)
                a = findAction(Q, s, epsilon_or_tau)

                # Take action a, observe r, s_prime
                r, s_prime, prey_caught = self.takeAction(s, a)                
                
                s = s_prime   
                                
            total_step_numbers += step_number
            
        average_number_of_steps = (total_step_numbers / float(X))
        
        return average_number_of_steps
     
    def deriveAction( self, Q, s, epsilon ):
        '''
        Find an action using Q, the current state, and epsilon, in an 
        epsilon-greedy fashion. 
        '''
        
        # Find the action that maximizes Q[(s, a)]                
        prob_actions = dict()        
        uniform_epsilon = epsilon / (len(self.actions))
        
        for possible_a in self.actions:
            # Set probabilities of all actions uniformly
            prob_actions[possible_a] = uniform_epsilon
        
        # Give the best action for this state a probability of 1
        best_a = argmax( Q[s] )
        prob_actions[best_a] += 1 - epsilon
                    
        # For every action, check if the cumulative probability exceeds a 
        # random number. 
        random_number = random.random()
        cumulative_prob = 0.0
        
        for a in self.actions:
            cumulative_prob += prob_actions[a]
            if cumulative_prob >= random_number:                
                return a
    
    def deriveActionSoftmax( self, Q, s, tau ):
        '''
        Find an action using Q, the current state s, and the temperature, 
        a measure similar to epsilon.
        '''        
        prob_actions = dict()
        
        # Determine the probability of each action
        denominator = 0
        for b in self.actions:
            denominator += exp(Q[s][b] / float(tau))

        for a in self.actions:
            numerator = exp(Q[s][a] / float(tau))
            prob_actions[a] = numerator / denominator
            
        # For every action, check if the cumulative probability exceeds a 
        # random number. 
        random_number = random.random()
        cumulative_prob = 0.0
        
        for a in self.actions:
            cumulative_prob += prob_actions[a]
            if cumulative_prob >= random_number:                
                return a

    def updatePolicyEpsilonGreedy( self, s, best_a, epsilon ):
        '''
        Given a state and the best action, this function sets the predators 
        policy so that in state s, the probability of taking action best_a is
        1.0 - epsilon + epsilon / N and probabilities of taking any other 
        actions are epsilon/N. 
        '''
        
        uniform_epsilon = epsilon / (len(self.actions))

        # Set probabilities of all actions except the best action uniformly
        for a in self.actions:
            self.policy[(s,a)] = uniform_epsilon
            
        # Give the new action for this state a probability of 1
        self.policy[(s,best_a)] += 1 - epsilon
      
    def takeAction( self, s, a ):
        ''' 
        Perform one step of the episode, given the current state and an action.
        '''
        # Udpate the state based on the predator's action
        s_new = self.performActionReduced(s, a)
        # Choose an action for the prey
        s_prime = self.Environment.Prey.simulateAction( s_new, reduced=True )
        # Determine the reward for the state-action-next_state pair
        r = self.Environment.reward(s, a, s_prime)
        # Check if the found state is terminal
        terminal = s_prime in self.Environment.terminal_states

        return r, s_prime, terminal
        
    def onPolicyMonteCarloControl( self, epsilon=0.1, gamma=0.8, max_iter=1000 ):
        
         # Initialize parameters        
        
        # Initialize S and V
        S,Terminal = self.Environment.getStates()
        A = self.actions

        # Create dictionaries for Q and Returns
        Q = self.init_Q()
        
        Returns = dict()
        for s in S:
            for a in A:
                Returns[(s,a)] = []
                self.policy[(s,a)] = 1.0 / len( A )
                
        s_start = (random.randint(-5,5),random.randint(-5,5))
        i = 0
        forever = True
        
        while forever:
            i += 1
            # Stop if a max number of iterations is reached
            forever = i < max_iter
            prey_caught = False
            episode = []
            s = s_start
            R = 0.0
            step = 0
            
            # (a) Generate episode using the current policy
            while not prey_caught:
                a = self.getAction( s )
                r, s_prime, prey_caught = self.takeAction( s, a )
                episode.append( (s,a) )
                s = s_prime
            
            # (b) For each pair (s,a) in the episode
            seen = set()
            step = len( episode ) - 1
            for s,a in episode:
                if s not in seen:
                    # Compute the return for this state
                    R = r * gamma ** step 
                    Returns[(s,a)].append( R )
                    Q[s][a] = sum(Returns[(s,a)]) / float(len(Returns[(s,a)]))
                    seen.add( s )
                step -= 1
                
            # (c) For each s in the episode
            for s,_ in episode:
                # Find the optimal action
                a_star = argmax( Q[s] )
                # Update the policy
                self.updatePolicyEpsilonGreedy( s, a_star, epsilon )
        return Q
