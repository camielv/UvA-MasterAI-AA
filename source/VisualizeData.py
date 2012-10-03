# Assignment:   Single Agent Learning
# Course:       Autonomous Agents 2012-2013
# Education:    Master Artificial Intelligence
# By:           Steven Laan
#               Auke Wiggers
#               Camiel Verschoor
#
# File:         VisualizeData.py
# Description:  Contains functions for plotting, smoothing of data.

import EnvironmentReduced
import numpy as np
import matplotlib.pyplot as plt

class VisualizeData():
    '''
    Class containing functions for visualization of data, smoothing..    
    '''    
    def __init__(self):
        self.Environment = EnvironmentReduced.EnvironmentReduced()
        self.Predator = self.Environment.Predator
        
    def plotPerformance(self,  method, episodes=250):
        '''
        Executes qlearning for different discount and learning rates, and plots
        the results. Possible methods are:
            self.Predator.onPolicyMonteCarloControl
            self.Predator.sarsa
            self.Predator.qLearning
        '''
        
        x = np.arange(0, episodes)
        
        for g in [0.1, 0.3, 0.5, 0.7, 0.9]:
            for a in [0.1, 0.2, 0.3, 0.4, 0.5]:
                print '\nPerformance measure of Qlearning for gamma = ' + \
                      '{0} and alpha = {1}'.format(g, a)

                Q, return_list = method(episodes=episodes,
                                        alpha=a, 
                                        gamma=g, 
                                        epsilon=0.1)
                
                return_list = self.smoothListTriangle(return_list, degree=10)
                                        
                plt.plot(x, np.array(return_list), label='Alpha {0}'.format(a))
            
            plt.legend()  
            plt.xlabel('Number of episodes')
            plt.ylabel('Number of steps taken')
            plt.title('The agent\'s performance (smoothed), gamma = {0}.'.format(g))
            plt.show()
        
    def plotSoftmaxPerformance(self, episodes=250):        
        '''
        Executes Q-learning for different temperatures, and plots the results.                
        '''
        x = np.arange(0, episodes)

        for t in [1,2,3,4,5]:
            Q, return_list = self.Predator.qLearning(episodes,
                                                     alpha=0.1,
                                                     gamma=0.7,
                                                     epsilon_or_tau=t,
                                                     epsilongreedy=False)
            return_list = self.smoothListTriangle(return_list, degree=10)
            
            plt.plot(x, np.array(return_list), label='Tau {0}'.format(t))
            
        plt.legend()  
        plt.xlabel('Number of episodes')
        plt.ylabel('Number of steps taken')
        plt.title('The agent\'s performance (using\nsoftmax action selection).')
        plt.show()
            
    def plotOptimisticInits(self, episodes=250):
        '''
        Executes Q-learning for different optimistic initializations of Q, and 
        plots the results.                
        '''
        x = np.arange(0, episodes)

        for c in [5, 15, 25]:
            Q, return_list = self.Predator.qLearning(episodes,
                                                     alpha=0.1,
                                                     gamma=0.7,
                                                     epsilon_or_tau=0.1,
                                                     epsilongreedy=True,
                                                     optimistic_value=c)
                                                     
            return_list = self.smoothListTriangle(return_list, degree=10)
            
            plt.plot(x, np.array(return_list), label='Initial value {0}'.format(c))
            
        plt.legend()  
        plt.xlabel('Number of episodes')
        plt.ylabel('Number of steps taken')
        plt.title('The agent\'s performance for different\ninitializations of Q')
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
