import environment

# Create the environment
e = environment.Environment()

# Add the first predator
e.addPredator( (0,0) )

# Counter for number of iterations
iterations = 0

# Start the simulation

while not e.caught:
    e.run()
    iterations += 1

print iterations