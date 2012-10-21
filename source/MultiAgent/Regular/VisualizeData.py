# Assignment:   MultiAgent Learning/Plannning
# Course:       Autonomous Agents 2012-2013
# Education:    Master Artificial Intelligence
# By:           Steven Laan
#               Auke Wiggers
#               Camiel Verschoor
#
# File:         VisualizeData.py
# Description:  Contains functions for plotting, smoothing of data.

from Environment import Environment
import numpy as np
import matplotlib.pyplot as plt

class VisualizeData():
    '''
    Class containing functions for visualization of data, smoothing..    
    '''    
    def __init__(self, environment=None, numberOfPredators=1):
        self.Environment = Environment(numberOfPredators=numberOfPredators) if \
            environment == None else environment
       
    def plotPerformance(self, episodes=10000, learning_rates=None):
        '''
        Executes qlearning for different discount and learning rates, and plots
        the results. Possible methods are:
            self.Predator.sarsa
            self.Predator.qLearning
        '''
        
        x = np.arange(0, episodes)
        
        print '\nExecuting performance measure of Q-Learning.'

        Q, return_list = self.Environment.qLearning(episodes, 10, True,
                                                    return_num_of_steps=True,
                                                    learning_rates=learning_rates)

        return_list = self.smoothListTriangle(return_list, degree=10)
                
        np.save( 'result', np.array( return_list ) )
                
        plt.plot(x, np.array(return_list))
        
        plt.xlabel('Number of episodes')
        plt.ylabel('Number of iterations')
        plt.title('Performance measure for all agents')
        plt.show()
    
    def plotReturn(self, episodes=100000, learning_rates=None):
        '''
        Executes qlearning for different discount and learning rates, and plots
        the results. Possible methods are:
            self.Predator.sarsa
            self.Predator.qLearning
        '''
        
        x = np.arange(0, episodes)
        
        print '\nExecuting performance measure of Q-Learning.'

        Q, return_list = self.Environment.qLearning(episodes, 10, True, 
                                                    return_num_of_steps=False,
                                                    learning_rates=learning_rates)
        print return_list        
        return_list = np.array(return_list)
        print return_list
        # The return for each agent is stored in columns
        prey_return = list(np.transpose(return_list[:,0]))
        prey_return = self.smoothListTriangle(prey_return, degree=10)
        plt.plot(x, np.array(prey_return), label='Prey')
        
        pred_return = np.transpose(return_list[:,1])
        pred_return = self.smoothListTriangle(pred_return, degree=10)
        plt.plot(x, np.array(pred_return), label='Predators')
                        
        plt.legend()
        plt.xlabel('Number of episodes')
        plt.ylabel('Number of iterations')
        plt.title('Performance measure for {0} agents'.format(self.Environment.numberOfPredators))
        plt.show()
         
    def smoothListLinear(self, input_list, degree=5):
        '''
        Smooths a given list input_list based on a degree, e.g. when input_list
        is [1,2,3,4] and degree = 1, the output will be a list containing the 
        mean of a subsection of 1 element plus 1 preceding plus 1 subsequent
        element.        
        '''        
        
        output_list = list()
        
        length = len(input_list)
        for index in xrange(length):
            selection = input_list[
                                   max(0, index-degree): 
                                   min(length, index + degree + 1)
                                   ]   
            output_list.append( sum(selection) / float(len(selection)) )         
        
        return output_list
            
    def smoothListTriangle(self, input_list, degree=5):  
        '''
        Smooths a given list input_list based on a triangle form, e.g. when
        the degree = 1, the output will be a list containing the weighted mean 
        of a subsection of 1 element plus 1 preceding plus 1 subsequent 
        element, where center elements have more weight.
        '''        
        weights = list()
        smoothed = list()
        for x in xrange(2*degree+1):
            weights.append(degree-abs(degree-x) + 1)  

        weights = np.array(weights)  

        length = len(input_list)
        for index in xrange(length):
            # Select a subset of the list            
            selection = np.array(
                                 input_list[
                                            max(0, index-degree): 
                                            min(length, index + degree + 1)
                                           ]
                                )
            # Select a subset of the weightlist, of equal size
            weight = np.array(
                             weights[
                                     max(degree-index,0):
                                     max(degree-index,0) + len(selection)
                                    ]
                             )
            smoothed.append(sum(selection* weight) / float(sum(weight)))
        return smoothed  

import sys
if __name__=="__main__":
    v = VisualizeData(numberOfPredators=int(sys.argv[1]))
    if len(sys.argv) == 3:
        print "Performing Q-Learning for {0} episodes.".format(sys.argv[2])
        v.plotPerformance(int(sys.argv[2]))
    if len(sys.argv) == 4:
        print "Performing Q-Learning with learning rates", sys.argv[3]
        v.plotPerformance(int(sys.argv[2]), eval(sys.argv[3]))
    
    
