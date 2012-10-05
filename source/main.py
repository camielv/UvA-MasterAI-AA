# Assignment:   Single Agent Planning
# Course:       Autonomous Agents 2012-2013
# Education:    Master Artificial Intelligence
# By:           Steven Laan         6036031
#               Auke Wiggers        6036163
#               Camiel Verschoor    6229298
#
# File:         main.py
# Description:  This file runs our implementation of all learning algorithms.

from EnvironmentReduced import EnvironmentReduced
import time

e = EnvironmentReduced()

# Execute Q-learning
now = time.time()
print '\n\nStarting Q-learning. \n\n'
Q, return_list = e.Predator.qLearning( episodes=1000, 
                                       alpha=0.5, 
                                       gamma=0.1,
                                       epsilon=0.1,
                                       epsilongreedy=True,
                                       optimistic_init=5 )
print 'Total time taken for 1000 episodes of Q-learning: \n{0} seconds.'.format(time.time() - now)
                      
print '\nFound values for Q[ state = (0,1) ]:'
for a in Q[(0,1)]:
    print 'Action {0}: \t {1}'.format(a, Q[(0,1)][a])   
print '\nAction (0,1) should approximate 10.0, all other actions 0.'
print '\nPress enter to continue.'
raw_input()



# Execute Q-learning using softmax
now = time.time()
print '\n\nStarting Q-learning using softmax. \n\n'
Q, return_list = e.Predator.qLearning( episodes=1000, 
                                       alpha=0.5, 
                                       gamma=0.1,
                                       epsilon=5,
                                       epsilongreedy=False,
                                       optimistic_init=5 )
print 'Total time taken for 1000 episodes of Q-learning using softmax\n'+ \
      'action selection: {0} seconds.'.format(time.time() - now)
                      
print '\nFound values for Q[ state = (0,1) ]:'
for a in Q[(0,1)]:
    print 'Action {0}: \t {1}'.format(a, Q[(0,1)][a])   
print '\nAction (0,1) should approximate 10.0, all other actions 0.'
print '\nPress enter to continue.'
raw_input()



# Execute sarsa
now = time.time()
print '\n\nStarting sarsa. \n\n'
Q, return_list = e.Predator.sarsa(episodes=1000, 
                                  alpha=0.5, 
                                  gamma=0.1, 
                                  epsilon=0.1, 
                                  optimistic_init=5 )

print 'Total time taken for 1000 episodes of sarsa: \n{0} seconds.'.format(time.time() - now)                      
print '\nFound values for Q[ state = (0,1) ]:'
for a in Q[(0,1)]:
    print 'Action {0}: \t {1}'.format(a, Q[(0,1)][a])    
print '\nAction (0,1) should approximate 10.0, all other actions 0.'
print '\nPress enter to continue.'
raw_input()


# Execute on-policy Monte Carlo
now = time.time()
print '\n\nStarting on-policy Monte Carlo. \n\n'
Q, return_list = e.Predator.onPolicyMonteCarloControl(episodes=1000,
                                                      epsilon=0.1,
                                                      gamma=0.1,
                                                      optimistic_init=5 )
                                                      
print 'Total time taken for 1000 episodes of on-policy Monte Carlo: \n{0} seconds.'.format(time.time() - now)                      
print '\nFound values for Q[ state = (0,1) ]:'
for a in Q[(0,1)]:
    print 'Action {0}: \t {1}'.format(a, Q[(0,1)][a])    
print '\nAction (0,1) should approximate 10.0, all other actions 0.\n\n'


print 'Standing still in state (1,0) is the second best action: \n'+\
      'the return will _very_ probably be a factor gamma 0.1 times as \n'+\
      'large as the best move. This is why sometimes, action (0,0) has a \n'+\
      'value that approximates 1.'
