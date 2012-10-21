import gurobipy as grb

A = set( ['rock','paper','scissors'] )
O = set( ['rock','paper','scissors'] )
s = 'state'

Q = dict()
Q[s] = dict()
for a in A:
    for o in O:
        Q[s][(a,o)] = 0
        
Q[s][('rock','paper')] = -1.0
Q[s][('scissors','rock')] = -1.0
Q[s][('paper','scissors')] = -1.0

Q[s][('paper','rock')] = 1.0
Q[s][('scissors','paper')] = 1.0
Q[s][('rock','scissors')] = 1.0


#Q[s][a,o] = (1-alpha) * Q[s][a,o] + alpha * (r + gamma* V[s_prime])

try:
    # Create a new model
    m = grb.Model("MultiAgentMinimax")
    m.setParam("OutputFlag",0)
    
    # Create variables
    pi = dict()
    for a in A:
        pi[a] = m.addVar( 0.0, 1.0, vtype = grb.GRB.CONTINUOUS, name = a )

    # Integrate new variables
    m.update()            

    # Set objective
    m.setObjective( grb.LinExpr( [ ( Q[s][(a,o)], pi[a] ) for o in O for a in A ] ), grb.GRB.MAXIMIZE)

    # Add constraint: Sum_a pi(a) = 1
    expr = grb.quicksum( m.getVars() )
    m.addConstr( expr == 1, "Total probability" )

    # Add more constraints
    for o in O:
        expr = grb.LinExpr( [ (Q[s][(a,o)], pi[a]) for a in A ] )
        m.addConstr( expr >= 0 )
    
    m.optimize()
    
    for v in m.getVars():
        print v.varName, v.x

    print 'Obj:', m.objVal

except grb.GurobiError:
    print 'Error reported'