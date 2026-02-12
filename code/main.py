from collections import Counter, defaultdict
import csv
from matplotlib import animation
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from heuristics import *
import models
import calc

MORE_STATS = True
SEED_RATIO = 0.05
FILENAMES = ["vilno_69.csv", "facebook_combined.txt", "Wiki-Vote.txt"]
FILES_TO_USE = [0]
HEURISTICS = [highest_degree, degree_discount, coreHD, random_selection, acquaintance]  # noqa: F405
HEU_ABR = ["HD", "DD", "CHD", "RND", "ACQ"]
BNCH_HEU = 3
HEUS_TO_USE = [0, 2, 3]
MODEL = models.threshold  # noqa: F405
NUM_ITERS = 100
RESEED = False # Run seeding algo every iteration for HD or every NUM_ITERS * RESEED_RATE iterations for CHD, DD
RESEED_RATE = 0.05

def load_graph(fn):
    fn = "data/" + fn
    if fn.endswith(".csv"):
        return load_matrix(fn)
    elif fn.endswith(".txt"):
        return load_edgelist(fn)
    else:
        ValueError("Unknown file extension")

def load_edgelist(fn):
    G = nx.read_edgelist(fn, comments = "#")
    return G

def load_matrix(fn):
    matrix = np.loadtxt(fn, delimiter=",")
    matrix = matrix.astype(int)
    G = nx.from_numpy_array(matrix)
    return G

def more_stats(G, i):
    print(f"File: {FILENAMES[i]}")
    print("Number of nodes read", G.number_of_nodes())
    print(f"Number of seed nodes: {int(G.number_of_nodes() * SEED_RATIO)}, ratio: {SEED_RATIO}")
    neighbors = [len(list(G.neighbors(node))) for node in G.nodes]
    neighbors.sort()
    print(neighbors)

    counts = Counter(neighbors)

    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)

    ax.scatter(counts.keys(), counts.values())
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel("Number of neighbors")
    ax.set_ylabel("Number of nodes")
    ax.set_title("Degree distribution")
    
    fig.show()

    # unactivated = G.nodes - set(activated.keys())
    # print([len(list(G.neighbors(node))) for node in unactivated])

def write_to_csv(results, fn, heu):
    file = "results/" + fn.replace(".csv", "") + "_" + heu + "_recencies.csv" 

    with open(file, "w", newline="") as f:
            writer = csv.writer(f)

            header = ["nodeID"] + [f"iter_{i + 1}" for i in range(len(results[0]))]
            writer.writerow(header)

            for node in sorted(results):
                writer.writerow([node] + results[node])

def run_simulations(G, heuristic, seed_num, num_iters=NUM_ITERS):
    results = defaultdict(list) # for each iteration: {nodeID : list{timestep}}

    seeds = heuristic(G, seed_num)

    for n in range(num_iters):
            # Currently set up to get a new seedset only on RND
            # For viz purposes, to highlight a constant seed set for HD

            if heuristic is random_selection:
                seeds = heuristic(G, seed_num)  # TODO: DD needs an additional param
            recency = MODEL(G, seeds, 0.1, 0.5)

            if n % 10 == 0 and MORE_STATS:
                print(f"{n} simulations run")

            for node in G.nodes:
                results[node].append(recency.get(node,"N"))

    return results

def simulate_all_permutations():
    for f in FILES_TO_USE:
        fn = FILENAMES[f]
        G : nx.Graph = load_graph(fn)
        seed_num = int((G.number_of_nodes() * SEED_RATIO))

        if MORE_STATS: 
            more_stats(G, f)

        for h in HEUS_TO_USE:
            heu = HEURISTICS[h]
            
            if MORE_STATS:
                print(f"Running {NUM_ITERS} simulations on {fn} using {heu}")

            results = run_simulations(G, heu, seed_num)
            write_to_csv(results, fn, HEU_ABR[h])

def run_calcs():
    bnch = HEU_ABR[BNCH_HEU]
    for f in FILES_TO_USE:
        fn = FILENAMES[f]
        for h in HEUS_TO_USE:
            heu = HEU_ABR[h]
            if bnch != heu:
                calc.calculate_ems(fn,heu,bnch)
            

def main():
    simulate_all_permutations()
    run_calcs()

if __name__ == "__main__":
    main()
