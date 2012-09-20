# Assignment:   Single Agent Planning
# Course:       Autonomous Agents 2012-2013
# Education:    Master Artificial Intelligence
# By:           Steven Laan         6036031
#               Auke Wiggers        6036163
#               Camiel Verschoor    6229298
#
# File:         main.py
# Description:  This file runs our implementation of the MDP.

from EnvironmentNormal import EnvironmentNormal
from EnvironmentReduced import EnvironmentReduced
from interface import Interface

def main():
    ''' Main function running single agent planning and the GUI '''
    # Initialize environment and get the begin state
    E = EnvironmentReduced()

    # Perform value iteration
    E.valueIteration()
    
    # Initialize Graphical User Interface with current state
    GUI = Interface( (11, 11) )
    GUI.start()

    print "Start simulation"
    # If the prey is not caught then run.
    while not E.predator.location == E.prey.location:
        # Run a step
        E.run()

        # If reload key 'r' is pressed restart
        if GUI.getReload():
            print "Reload simulation"
            E.reset()
       
        # Set new locations in GUI
        GUI.setPredator( E.predator.location )
        GUI.setPrey( E.prey.location )

        if GUI.getStatus():
            break
        
    # Wait for exit event in GUI.
    GUI.join()
    del GUI

# If this is the main script run main function
if __name__ == '__main__':
    main()
