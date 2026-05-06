import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

class plot:
    def __init__(self):
        pass
        
    def pyplot(self, G, n, p):
        pos = nx.spring_layout(G, 2)
        nx.draw_networkx(
            G, pos, 
            font_color='white', font_size=14, node_size=400,
            width=1.5
        )

        plt.title(f"Graph Output - ($n = {n}, p = {p}$)")
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

        [mis_nodes, match_edges, perf_match_edges, cliques] = data_object.get_results()

        domination_sets = []
        domination_number = None
        if hasattr(data_object, 'get_domination_results'):
            dom_results = data_object.get_domination_results()
            if isinstance(dom_results, tuple) and len(dom_results) >= 1:
                domination_sets = dom_results[0] or []
                if len(dom_results) >= 2:
                    domination_number = dom_results[1]
        elif hasattr(data_object, 'domination_sets'):
            domination_sets = getattr(data_object, 'domination_sets') or []
        elif hasattr(data_object, 'domination_number'):
            domination_number = getattr(data_object, 'domination_number')

        if domination_number is None and domination_sets:
            valid_sizes = [len(s) for s in domination_sets if s is not None]
            if valid_sizes:
                domination_number = min(valid_sizes)

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
        plt.title('Node Appearance Count - Maximum Stable Set')
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

        match_heat = pair_heat.copy()

        ## Cliques
        clique_size_count = {}
        for clique in cliques:
            if clique is None:
                continue
            clique_size = len(clique)
            clique_size_count[clique_size] = clique_size_count.get(clique_size, 0) + 1

        if clique_size_count:
            sizes = sorted(clique_size_count.keys())
            counts = [clique_size_count[size] for size in sizes]
            
            plt.figure(figsize=(10, 5))
            colors = plt.cm.viridis(np.linspace(0.2, 0.8, len(sizes)))
            plt.bar([f'K{size}' for size in sizes], counts, color=colors)
            plt.xlabel('Clique Size')
            plt.ylabel('Appearance Count')
            plt.title('Maximum Clique Appearance by Size')
            plt.tight_layout()
            plt.show()

        ## Domination Number
        if domination_number is not None:
            plt.figure(figsize=(6, 4))
            plt.bar(['Domination Number'], [domination_number], color='darkgreen')
            plt.ylabel('Number of Nodes')
            plt.title('Domination Number')
            plt.tight_layout()
            plt.show()

        if domination_sets:
            domination_size_count = {}
            for dom_set in domination_sets:
                if dom_set is None:
                    continue
                dom_size = len(dom_set)
                domination_size_count[dom_size] = domination_size_count.get(dom_size, 0) + 1

            if domination_size_count:
                sizes = sorted(domination_size_count.keys())
                counts = [domination_size_count[size] for size in sizes]
                plt.figure(figsize=(10, 5))
                plt.bar([f'D{size}' for size in sizes], counts, color='seagreen')
                plt.xlabel('Domination Set Size')
                plt.ylabel('Appearance Count')
                plt.title('Domination Set Appearance by Size')
                plt.tight_layout()
                plt.show()

        ## Matchings and Perfect Matchings
        node_order = sorted(nodes, key=lambda x: str(x))
        node_to_idx = {n: i for i, n in enumerate(node_order)}
        pair_heat = np.zeros((len(node_order), len(node_order)), dtype=int)

        for matching in perf_match_edges:
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

        perfect_heat = pair_heat.copy()

        fig, axes = plt.subplots(1, 2, figsize=(16, 6), sharex=True, sharey=True)

        im0 = axes[0].imshow(match_heat, cmap='viridis', interpolation='nearest')
        axes[0].set_title('Heat Map of Edge (Node Pair) Matchings')
        axes[0].set_xlabel('Node')
        axes[0].set_ylabel('Node')
        axes[0].set_xticks(range(len(node_order)))
        axes[0].set_xticklabels([str(n) for n in node_order], rotation=90)
        axes[0].set_yticks(range(len(node_order)))
        axes[0].set_yticklabels([str(n) for n in node_order])
        fig.colorbar(im0, ax=axes[0], label='Matching Co-Occurrence Count')

        im1 = axes[1].imshow(perfect_heat, cmap='viridis', interpolation='nearest')
        axes[1].set_title('Heat Map of Edge (Node Pair) Perfect Matchings')
        axes[1].set_xlabel('Node')
        axes[1].set_ylabel('Node')
        axes[1].set_xticks(range(len(node_order)))
        axes[1].set_xticklabels([str(n) for n in node_order], rotation=90)
        axes[1].set_yticks(range(len(node_order)))
        axes[1].set_yticklabels([str(n) for n in node_order])
        fig.colorbar(im1, ax=axes[1], label='Perfect Matching Co-Occurrence Count')

        plt.tight_layout()
        plt.show()

        