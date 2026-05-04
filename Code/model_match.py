import gurobipy as gp
from gurobipy import GRB

import networkx as nx

class match_model:
    def __init__(self):
        self.model = gp.Model("pm_model")
        self.model.setParam("OutputFlag", 0)                            ## Prevent all comments from spamming terminal
        self.set_soln_set = []
        self.set_soln_weights = []

    def optimize(self, Graph):
        V, E = list(Graph.nodes()), list(Graph.edges())

        ## Define decision variables
        x = self.model.addVars(E, lb=0.0, ub=1.0, vtype=GRB.BINARY, name="DV: x")
        
        ## Objective: minimize sum of selected nodes
        self.model.setObjective(gp.quicksum(x[e] for e in E), GRB.MAXIMIZE)

        ## Constraint: Degree 
        self.model.addConstrs(((gp.quicksum(x[e] for e in E if v in e) <= 1) for v in V), name="degree")

        ## Optimize!
        self.model.optimize()

        if self.model.status == GRB.OPTIMAL:
            self.set_soln_set = [e for e in E if x[e].X >= 0.5]
            self.set_soln_weights = [(e, x[e].X) for e in E if x[e].X >= 0.5]
        else:
            self.set_soln_set = []
            self.set_soln_weights = []

    def opt_cost(self): return self.model.ObjVal

    def opt_soln(self): return self.set_soln_set, self.set_soln_weights