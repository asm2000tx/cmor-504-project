import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

class plot:
    def __init__(self):
        pass
        
    def pyplot(self, G):
        pos = nx.spring_layout(G, 2)
        nx.draw_networkx(
            G, pos, 
            font_color='white', font_size=14, node_size=400,
            width=1.5
        )

        plt.title(f"Graph Output")
        plt.show()

    def pyplot_append_caption_debug(self, G, lvl, v):
        pos = nx.spring_layout(G, 2)
        nx.draw_networkx(
            G, pos, 
            font_color='white', font_size=14, node_size=400,
            width=1.5
        )

        plt.title(f"Graph Output - Level {lvl} at Node {v}")
        plt.show()

    def pyplot_depth_visual(self, graph_count, rec_level):
        plt.figure(figsize=(12, 5))
    
        plt.subplot(1, 2, 1)
        plt.plot(graph_count, color='blue', label='Graph Count')
        plt.xlabel('Index')
        plt.ylabel('Graph Count')
        plt.title('Graph Count')
        plt.legend()

        plt.subplot(1, 2, 2)
        plt.plot(rec_level, color='orange', label='Recursion Level')
        plt.xlabel('Index')
        plt.ylabel('Recursion Level')
        plt.title('Recursion Level')
        plt.legend()
            
        plt.tight_layout()
        plt.show()

    def plot_results(self, graph, data_object):
        nodes = list(graph.nodes())

        [mis_nodes, match_edges, 
         perf_match_val, perf_match_edges, cliques] = data_object.get_results()

        ## Maximum Stable Set Plot
        node_dict = {}
        appeared_nodes = set()
        for mis_set in mis_nodes:
            for v in mis_set:
                appeared_nodes.add(v)
                node_dict[v] = node_dict.get(v, 0) + 1

        self.appeared_nodes = sorted(appeared_nodes, key=lambda x: str(x))
        self.node_appearance_count = node_dict

        node_labels = [str(n) for n in self.appeared_nodes]
        node_counts = [node_dict[n] for n in self.appeared_nodes]

        plt.figure(figsize=(10, 5))
        plt.bar(node_labels, node_counts, color='steelblue')
        plt.xlabel('Nodes')
        plt.ylabel('Head Count / Appearance')
        plt.title('Node Appearance Count')
        plt.tight_layout()
        plt.show()

        ## Matchings
        node_order = sorted(nodes, key=lambda x: str(x))
        node_to_idx = {n: i for i, n in enumerate(node_order)}
        pair_heat = np.zeros((len(node_order), len(node_order)), dtype=int)

        for matching in match_edges:
            if matching is None:
                continue
            for edge in matching:
                if edge is None or len(edge) < 2:
                    continue
                u, w = edge[0], edge[1]
                if u in node_to_idx and w in node_to_idx:
                    i, j = node_to_idx[u], node_to_idx[w]
                    pair_heat[i, j] += 1
                    pair_heat[j, i] += 1

        plt.figure(figsize=(8, 6))
        im = plt.imshow(pair_heat, cmap='viridis', interpolation='nearest')
        plt.colorbar(im, label='Matching Co-Occurrence Count')
        plt.xticks(range(len(node_order)), [str(n) for n in node_order], rotation=90)
        plt.yticks(range(len(node_order)), [str(n) for n in node_order])
        plt.xlabel('Node')
        plt.ylabel('Node')
        plt.title('Heat Map of Node-Pair Appearances in Matchings')
        plt.tight_layout()
        plt.show()

    # self.mis_nodes.append(mis_soln)
    # self.matching_edges.append(match_soln)
    # self.perfect_matching_num.append(perf_match_soln)
    # self.perfect_matching_edges.append(perf_match_edges)
    # self.clique_set.append(clique_soln)


    # pos options: 
    # - nx.spring_layout
    # - nx.circular_layout

    # nx.draw_networkx(
    #     G, pos, 
    #     ## Node adjustment - font_color, font_size, node_size
    #     ## Edge adjustment - width
    # )
