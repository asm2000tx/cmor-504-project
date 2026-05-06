import networkx as nx

from model_match import match_model
from model_max_is import max_ind_set_model
from model_match_perf import perfect_match_model

class result_generation:
    def __init__(self):
        ## Maximum Independence 
        self.mis_nodes = []
        self.mis_cost = []

        ## Matchings
        self.matching_edges = []
        self.matching_num = []

        ## Perfect Matchings
        self.perfect_matching_num = []
        self.perfect_matching_edges = []

        ## Cliques
        self.clique_set = []
        self.clique_num = []

    def data_collection(self, G):
        mis_model = max_ind_set_model()                     ## Maximum independent set
        mis_model.optimize(G)
        mis_soln, _ = mis_model.opt_soln()

        matching_model = match_model()                      ## Matchings
        matching_model.optimize(G)
        match_soln, _ = matching_model.opt_soln()

        perf_matching_model = perfect_match_model()         ## Perfect matchings
        perf_matching_model.optimize(G)
        perf_match_edges, perf_match_soln = perf_matching_model.opt_soln()
        
        G_comp = nx.complement(G)
        max_clique_model = max_ind_set_model()              ## Maximum clique
        max_clique_model.optimize(G_comp) 
        clique_soln, _ = max_clique_model.opt_soln()    

        # print("\n" + "="*50)
        # print("RESULTS SUMMARY")
        # print("="*50)
        
        # print("\n[1] Maximum Stable Set on Graph G:")
        # print(f"    Nodes: {mis_soln}")
        
        # print("\n[2] Matchings on Graph G:")
        # print(f"    Edges: {match_soln}")
        
        # print("\n[3] Perfect Matching on G:")
        # print(f"    Edges: {perf_match_edges}")
        # print(f"    Solution: {perf_match_soln}")
        
        # print("\n[4] Maximum Clique on G:")
        # print(f"    Nodes: {clique_soln}")
        
        # print("\n" + "="*50 + "\n")

        self.mis_nodes.append(mis_soln)
        self.matching_edges.append(match_soln)
        self.perfect_matching_num.append(perf_match_soln)
        self.perfect_matching_edges.append(perf_match_edges)
        self.clique_set.append(clique_soln)

    def get_results(self):
        return [self.mis_nodes, self.matching_edges, self.perfect_matching_edges, self.clique_set]