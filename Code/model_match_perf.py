import gurobipy as gp
from gurobipy import GRB

import networkx as nx

class perfect_match_model:
    def __init__(self):
        self.model = gp.Model("pm_model")
        self.model.setParam("OutputFlag", 0)                            ## Prevent all comments from spamming terminal
        
        self.set_soln_edges = []
        self.set_soln_weights = []

    def optimize(self, Graph):
        V, E = list(Graph.nodes()), list(Graph.edges())

        ## Define decision variables
        x = self.model.addVars(E, lb=0.0, ub=1.0, vtype=GRB.CONTINUOUS, name="DV: x")
        
        ## Objective: minimize sum of selected nodes
        self.model.setObjective(gp.quicksum(x[e] for e in E), GRB.MAXIMIZE)

        ## Constraint: Degree 
        self.model.addConstrs(((gp.quicksum(x[e] for e in E if v in e) == 1) for v in V), name="degree constraint")
        
        ## Optimize!
        self.model.optimize()
        
        status = False
        if self.model.status == GRB.OPTIMAL: 
            self.set_soln_edges = [i for i in E if x[i].X > 0]
            for i in self.set_soln_edges: self.set_soln_weights.append(x[i].X)
            status = True

        if status:
            vals = self.set_soln_weights
            tol = 1e-6
            n0  = sum(1 for v in vals if abs(v - 0.0) <= tol)
            n05 = sum(1 for v in vals if abs(v - 0.5) <= tol)
            n1  = sum(1 for v in vals if abs(v - 1.0) <= tol)
            label = "Feasible"

        # if status: print(f"{label} | count(x=0): {n0}, count(x=0.5): {n05}, count(x=1): {n1}")

    def opt_cost(self): return self.model.ObjVal

    def opt_soln(self): return self.set_soln_edges, self.set_soln_weights