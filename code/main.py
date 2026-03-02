from collections import defaultdict
import csv
import networkx as nx
from utils import load_graph
from heuristics import *  # noqa: F403
import models
import calc

MORE_STATS = True
SEED_RATIO = 0.02
FILENAMES = ["vilno_69.csv", "facebook_combined.txt", "Wiki-Vote.txt"]
FILES_TO_USE = [1]
HEURISTICS = [highest_degree, degree_discount, coreHD, random_selection, acquaintance]  # noqa: F405
HEU_ABR = ["HD", "DD", "CHD", "RND", "ACQ"]
HEUS_TO_USE = [0,3]
BNCH_HEU = 3
MODEL = models.threshold_norm  # noqa: F405
NUM_ITERS = 100
RESEED = False   # Run seeding algo every iteration for HD or every NUM_ITERS * RESEED_RATE iterations for CHD, DD
                # RND always reseeded
RESEED_RATE = 0.05
THRESHOLDS = [(0.2,0.2)]

def write_to_csv(results, fn, heu, kl, ku):
    fn = fn.replace(".csv", "")
    fn = fn.replace(".txt", "")
    fn = f"results/{fn}_{heu}_{int(SEED_RATIO*100)}_seed_{int(kl*100)}_{int(ku*100)}_thres.csv"

    with open(fn, "w", newline="") as f:
            writer = csv.writer(f)

            header = ["nodeID"] + [f"iter_{i + 1}" for i in range(NUM_ITERS)]
            writer.writerow(header)
            
            for node in sorted(results):
                writer.writerow([node] + results[node])

def should_reseed(heuristic, seeds, n):

    if heuristic == random_selection:
        return True
    elif not seeds:
        return True
    elif RESEED:
        if heuristic == highest_degree:
            return True
        elif heuristic in [coreHD, degree_discount] and n % int(RESEED_RATE * NUM_ITERS) == 0:
            return True
    
    return False

def simulate_all_permutations():

    # For each dataset
    for f in FILES_TO_USE:
        fn = FILENAMES[f]
        G : nx.Graph = load_graph(fn)
        seed_num = int((G.number_of_nodes() * SEED_RATIO))
        if MORE_STATS: 
            print(f"File: {fn}")
            print("Number of nodes read", G.number_of_nodes())
            print(f"Number of seed nodes: {seed_num}, ratio: {SEED_RATIO}")

        # For each heuristic
        for h in HEUS_TO_USE:
            heu = HEURISTICS[h]
            if MORE_STATS:
                print(f"Running {NUM_ITERS} simulations on {fn} using {heu}")

            # For each pair of thresholds, final permutation
            for kl, ku in THRESHOLDS:

                # New set of results and seed nodes:
                results = defaultdict(list)
                seeds = set()
                
                # Simulations
                for n in range(NUM_ITERS):
                    if should_reseed(heu, seeds, n):
                        seeds = heu(G, seed_num, p_infection=0.3)

                    recency = MODEL(G, seeds, 0.4)   # Run actual simulation

                    if n % 10 == 0 and MORE_STATS:
                        print(f"{n} simulations run")

                    for node in G.nodes:
                        results[int(node)].append(recency.get(node,"")) # can have default as NaN once refactored to pkl

                # Write results of each permutation to csv
                write_to_csv(results, fn, HEU_ABR[h], kl, ku)

def run_calcs():
    bnch = HEU_ABR[BNCH_HEU]
    for f in FILES_TO_USE:
        fn = FILENAMES[f]
        for h in HEUS_TO_USE:
            heu = HEU_ABR[h]
            for kl, ku in THRESHOLDS:
                if bnch != heu:
                    calc.calculate_ems(fn,heu,bnch, kl, ku, SEED_RATIO)
            

def main():
    simulate_all_permutations()
    run_calcs()

if __name__ == "__main__":
    main()
