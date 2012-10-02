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
import csv

class VisualizeData():
    '''
    Class containing functions for visualization of data, smoothing..    
    '''    
    def __init__(self):
        self.Environment = EnvironmentReduced.EnvironmentReduced()
        self.Predator = self.Environment.Predator
        
    def plotPerformance(self, episodes=500, save_data=True):
        '''
        Executes a given function for different discount alpha, gamma, epsilon
        '''
        some_range = np.arange(0.1, 0.31, 0.2)
        x = np.arange(0, episodes)
        epsilon = 0.1
        
        
        for gamma in some_range:
            i = 0
            for alpha in some_range:
                print '\nPerformance measure of Qlearning for gamma = ' + \
                      '{0} and alpha = {1}'.format(gamma, alpha)

                      
                Q, return_list = self.Predator.qLearning(alpha, 
                                                         gamma, 
                                                         epsilon, 
                                                         episodes)
                i += 1
                
                return_list = self.smoothListTriangle(return_list, degree=10)
                                        
                if save_data:
                    print return_list
                    for i in xrange(len(return_list)):
                        return_list[i] = str(return_list[i])
                    with open('performance.csv', 'wb') as f:
                        writer = csv.writer(f)
                        writer.writerow(return_list)
                        
                else:
                    plt.plot(x, np.array(return_list), label='Alpha {0}'.format(alpha))
            if not save_data:
                plt.legend()  
                plt.xlabel('Number of episodes')
                plt.ylabel('Number of steps taken')
                plt.title('The agent\'s performance (smoothed), gamma = {0}.'.format(gamma))
                plt.show()
            else:
                with open('performance.csv', 'wb') as f:
                    writer = csv.writer(f)
                    writer.writerow([])
        
            
    def smoothListLinear(self, input_list, degree=5):
        '''
        Smooths a given list input_list based on a degree, e.g. when input_list
        is [1,2,3,4] and degree = 1, the output will be a list containing the 
        mean of a subsection of 1 element plus 1 preceding plus 1 next element.        
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
        Smooths a given list input_list based on a triangle, e.g. when
        input_list is [1,2,3,4] and degree = 1, the output will be a list 
        containing the weighted mean of a subsection of 1 element plus 1 
        preceding plus 1 next element, where center elements have more weight.
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
