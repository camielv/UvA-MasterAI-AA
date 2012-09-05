import environment

# Counter for number of iterations
total = 0
N = 100

# Start the simulation
for i in xrange( N ):

    iterations = 0
    # Create the environment
    e = environment.Environment()
    
    # Add the first predator
    e.addPredator( (0,0) )
    iterations = 0    
    
    while not e.caught:
        e.run()
        iterations += 1
    total += iterations

print 'Averge number of iterations:', total / float( N )
    