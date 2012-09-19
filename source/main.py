from EnvironmentNormal import EnvironmentNormal
from EnvironmentReduced import EnvironmentReduced
from interface import interface

def main():
    ''' Main function running single agent planning and the GUI '''
    # Initialize environment and get the begin state
    E = EnvironmentNormal()
    s = E.getState()

    # Initialize Graphical User Interface with current state
    GUI = Interface( (11, 11), s )
    GUI.start()

    # Decode the state
    pred_x, pred_y, prey_x, prey_y = s

    # If the prey is not caught then run.
    while( not( (pred_x, pred_y) == (prey_x, prey_y) ) ):
        # Run a step
        E.run()
        s = E.getState()

        pred_x, pred_y, prey_x, prey_y = s

        # Set new locations in GUI
        GUI.setPredator( (pred_x, pred_y) )
        GUI.setPrey( (prey_x, prey_y) )

    # Wait for exit event in GUI.
    GUI.join()

# If this is the main script run main function
if( __name__ == '__main__' ):
    main()


'''
Old shit!!!!!!!!!!!!!!!
# Counter for number of iterations
total = 0
N = 100

for i in xrange( N ):

    iterations = 0
    # Create the environment
    e = environment.Environment()
    
    # Add the first predator
    e.addPredator( (0,0) )
    iterations = 0    
    
    # Perform simulation
    while not e.caught:
        e.run()
        iterations += 1
    total += iterations

print 'Averge number of iterations:', total / float( N )
''' 
