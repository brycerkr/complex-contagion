import math
import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.colors as mplc
import matplotlib.ticker as mticker
from utils import load_graph, load_pickle_file

DEBUG = True

# Load graph
G = load_graph("datasets/village.csv")

# Basic graph setup:
fig, ax = plt.subplots(figsize=(8, 8))
pos = nx.spring_layout(G, seed=42, k=0.6, iterations=80)

# START COMPUTING COLORS

#Read file in 
""" df = pd.read_csv("calcs/facebook_combined_HD_RND_2_seed_5_20_thres_calcs.csv")
effective_measures = dict(zip(df["nodeID"], df["effective_tau"]))
non_seed_ems = df[df["seed_node"] == 0]["effective_tau"].to_numpy()

vmax = math.ceil(non_seed_ems.max())
vmin = non_seed_ems.min() """

em_data = load_pickle_file("em_results/village/threshold_norm/mean_0.5_std_0.2/HD_effective_measures.pkl")
effective_measures = dict(zip(em_data["nodeID"], em_data["em_frequency"]))

# print(effective_measures)
em_list = list(effective_measures.values())
filtered = filter(lambda x : x != 0, em_list)
em_list = list(filtered)

vmax = math.ceil(max(em_list))
vmin = min(em_list)

print(f"vmin: {vmin}, vmax:{vmax}")

norm = mplc.TwoSlopeNorm(1, vmin,vmax)

cmap = plt.cm.PuOr

node_colors = [effective_measures.get(node, 0) for node in G.nodes]
mapped_colors = [cmap(norm(v)) for v in node_colors]

nodes = nx.draw_networkx_nodes(
    G,
    pos,
    ax=ax,
    node_color=mapped_colors,
    node_size=100,
)

""" seed_nodes = dict(zip(df["nodeID"], df["seed_node"]))
seed_nodes_list = [n for n in G.nodes if seed_nodes.get(n, 0) == 1]

nx.draw_networkx_nodes(
    G,
    pos,
    nodelist=seed_nodes_list,
    node_color="black",
    node_size=100,
    ax=ax,
) """

nodes.set_edgecolor("black")
nodes.set_linewidth(0.3)

nx.draw_networkx_edges(G, pos, ax=ax, alpha=0.1, width=1, edge_color="grey")

ax.axis("off")

sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
sm.set_array([])


# COLORBAR CODE
cbar = plt.colorbar(sm, ax=ax, shrink=0.8)

num_ticks = 7  # adjust for more/less ticks

# equidistant ticks
ticks = np.logspace(np.log10(vmin), np.log10(vmax), num_ticks)
cbar.set_ticks(ticks)

# Format ticks as plain numbers
cbar.ax.yaxis.set_major_formatter(mticker.FuncFormatter(
    lambda x, _: f"{x:.2g}"
))

cbar.set_label("τ_HD / τ_benchmark", rotation=270, labelpad=15)

""" if DEBUG:
    above_1 = np.sum(non_seed_ems > 1)
    below_1 = np.sum(non_seed_ems < 1)

    print(f"Values above 1: {above_1}")
    print(f"Values below 1: {below_1}")
    print(f"Max em: {vmax}")
    print(f"Min em: {vmin}") """

plt.show()
