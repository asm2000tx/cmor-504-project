import sys
import networkx as nx

sys.setrecursionlimit(10**6)

class orbit:
    def __init__(self, mod_len):
        self.graph_list = set() # Graphs seen in the recursion and non-isomorphic to one another 
        self.mod_len = mod_len

        self.iter_count = 0
        self.max_rec_lvl = 0
        self.output_list = []  # entries: (phase, level, graph_count)

    def isomorphic_status(self, G):
        for graph in self.graph_list: 
            if nx.is_isomorphic(G, graph): 
                # print("\nGraph is isomorphic ...\n")
                return True
        return False
    
    def gen_local_complement(self, G, neighbors_v):
        ## Generate the local complement of the open neighborhood at node v
        G_local_comp = nx.complement(nx.induced_subgraph(G, neighbors_v))

        ## Generate local copy of the graph 
        G_update = G.copy()

        ## Remove local edges from original graph
        edges_to_remove = [(s,t) for s,t in G.edges if s in neighbors_v and t in neighbors_v]
        G_update.remove_edges_from(edges_to_remove)

        ## Appending local complement edges to graph copy and perform recursion
        G_update.add_edges_from(list(G_local_comp.edges))

        # print("\nGoing up one recursive level ...\n")

        return G_update
    
    def gen_orbits(self, G, lvl):

        ## Update to maximum recursion level
        if self.max_rec_lvl < lvl: self.max_rec_lvl = lvl

        ## Check if the current graph G is isomorphic
        if self.isomorphic_status(G): return
        self.graph_list.add(G)

        ## Collect information if G is non-isomorphic (Pre-Recursion)
        if lvl % self.mod_len == 0:
            print(f"[PRE] Current level: {lvl} - Graph count: {len(self.graph_list)}")
            self.output_list.append((len(self.graph_list), lvl))

        for v in list(G.nodes):
            neighbors_v = list(nx.all_neighbors(G, v))
            if len(neighbors_v) <= 1: continue

            G_update = self.gen_local_complement(G, neighbors_v)
            self.gen_orbits(G_update, lvl + 1)

        ## Collect information if G is non-isomorphic (Post-Recursion)
        if lvl % self.mod_len == 0:
            print(f"[POST] Current level: {lvl} - Graph count: {len(self.graph_list)}")
            self.output_list.append((len(self.graph_list), lvl))

    def collect_results(self): return self.graph_list, self.output_list
