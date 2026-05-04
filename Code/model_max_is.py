import gurobipy as gp
from gurobipy import GRB, quicksum

import networkx as nx

class max_ind_set_model:
    def __init__(self):
        self.model = gp.Model("mis_model")
        self.model.setParam("OutputFlag", 0)                            ## Prevent all comments from spamming terminal
        
        self.set_soln_nodes = []
        self.set_soln_weights = []

    def optimize(self, Graph):
        V, E = list(Graph.nodes()), list(Graph.edges())

        ## Define decision variables
        x = self.model.addVars(V, lb=0.0, ub=1.0, vtype=GRB.BINARY, name="DV: x")

        ## Define edge constratins
        for [u, v] in E: self.model.addConstr(x[u] + x[v] <= 1, f"C1: ({u},{v})")

        ## Defining the cost coefficient vector
        c = [1] * len(V)
        
        ## Objective Function: max c'x
        objective = gp.quicksum(c[v] * x[v] for v in V)
        self.model.setObjective(objective, gp.GRB.MAXIMIZE)
    
        ## Perform optimization
        self.model.optimize()

        ## Find the solution
        for node, var in x.items():
            if var.X > 0.5:
                self.set_soln_nodes.append(node)
                self.set_soln_weights.append(var.X)

    def opt_cost(self): return self.model.ObjVal

    def opt_soln(self): return self.set_soln_nodes, sum(self.set_soln_weights)