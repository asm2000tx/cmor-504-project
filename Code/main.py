import sys
import time
import networkx as nx
import matplotlib.pyplot as plt

from plot import plot
from orbit import orbit
from data_generation import result_generation

sys.setrecursionlimit(10**6)

def main() -> int:
    G = nx.erdos_renyi_graph(8, 0.55)

    plot_graph = plot()
    plot_graph.pyplot(G)

    mod_len = 10
    orbit_graph = orbit(mod_len)

    start = time.perf_counter()
    orbit_graph.gen_orbits(G, 1)
    end = time.perf_counter()

    graph_list, output_list = orbit_graph.collect_results()
    # print(f"\nFinal graph count: {len(graph_list)}")

    time_diff = (end - start)
    if time_diff / 60 < 1: print(f"Time taken: {time_diff:.2f} seconds\n")
    else: print(f"Time taken: {time_diff / 60:.2f} minutes\n")

    graph_count, rec_level = [], []
    for k in range(len(output_list)):
        graph_count.append(output_list[k][0])
        rec_level.append(output_list[k][1])

    plot_graph.pyplot_depth_visual(graph_count, rec_level)

    data_object = result_generation()
    for graph in graph_list:
        data_object.networx_data_collection(graph)
        data_object.gurobipy_data_collection(graph)

    # plot_graph.plot_results(graph, data_object)

    return 0

if __name__ == "__main__":
    raise SystemExit(main())
