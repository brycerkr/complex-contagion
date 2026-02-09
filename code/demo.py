from collections import defaultdict
import random
import networkx as nx

def highest_degree(G, seed_num):
    """
    Returns seed_num nodes with highest degree in G.
    
    :param G: Graph
    :param seed_num: Size of desired set
    """
    # find the minimum value of k for the number of seed nodes
    k_min = min(sorted(dict(G.degree()).values(), reverse=True)[:seed_num])
        
    # select all nodes with k above k_min
    high_k_nodes = [n for n, k in dict(G.degree()).items() if k > k_min]

    # select all nodes with k = k_min
    k_min_nodes = [n for n, k in dict(G.degree()).items() if k == k_min]

    # nodes we need randomly pick from k_min_nodes to meet seed size
    sample_size = seed_num - len(high_k_nodes)

    # select seed nodes and update seed statistics
    seed_nodes_ = high_k_nodes + random.sample(k_min_nodes, sample_size)

    seed_nodes = set(seed_nodes_)  # for fast lookup
    return seed_nodes

def coreHD(G,seeds):
    H = G.copy().copy()
    H.remove_edges_from(nx.selfloop_edges(H))
    seed_nodes = []
    for i in range(seeds):
        print("coreHD iter ", i)
        # find k=2 core
        kcore = nx.k_core(H, k=2)

        # find node or nodes with max degree node
        k_max = max(dict(kcore.degree()).values())

        # if mode candidates pick random node
        node = random.choice([n for n, k in dict(kcore.degree()).items() if k == k_max])

        H.remove_node(node)
        seed_nodes.append(node)

    return set(seed_nodes)

def ICM(G, seed_nodes_, p_infection):
    '''
        Independent cascade model
        ------------------
        Input:
        * G: directed opr undirected network
        * seed_nodes_: list of seed nodes or number of initial seeds to simulate the dynamics from
        * p: infection/spreading probability
        ------------------
        Output:
        * for activated node, timestamp of when they were activated
        ------------------
        '''
    # if type(seeds) != list:
    # infected = set(random.sample(network.nodes(),seeds)) # infect seeds
    # else:
    infected = set(seed_nodes_)

    activated = infected.copy()
    activation_time = defaultdict(int)

    # add initial seed to activated & activation_time
    for n in infected:
        activation_time[n] = 0

    t = 1
    # run infection process
    while infected != set():
        new_infected = set()
        for node in infected:
            # print node
            for neighbor in G.neighbors(node):
                # print "--- ",neighbor
                r = random.random()
                # print "--- ",r
                if (r < p_infection) and (neighbor not in activated):
                    # register activation time
                    activation_time[neighbor] = t

                    # update sets
                    new_infected.add(neighbor)
                    # print "--- infected"
                    activated.add(neighbor)  # add node here to prevent newly infected nodes to be infected again

        # set of newly infected nodes
        infected = new_infected.copy()

        # update time counter
        t += 1

    # return list of infected/recovered nodes
    return activation_time

def threshold(G, activated, k):

    remaining = set(G.nodes) - activated
    activation_edges = set()

    activation_time = defaultdict(int)

    print("Starting threshold simulation")

    t = 1

    while True:

        new_infected = set()

        for node in remaining:
            infected_neighbors = 0
            for neighbor in G.neighbors(node):
                if neighbor in activated:
                    infected_neighbors += 1
            if infected_neighbors >= k:
                
                new_infected.add(node)
                activation_time[node] = t
                
                for neighbor in G.neighbors(node):
                    activation_edges.add((node,neighbor))

        if not new_infected:
            break
        
        t += 1
        remaining -= new_infected
        activated |= new_infected
    
    return activation_time

def threshold_range(G, activated, kl, ku):

    remaining = set(G.nodes) - activated
    activation_edges = set()

    activation_time = defaultdict(int)

    print("Starting threshold simulation")

    thresholds = defaultdict(int)

    for node in G.nodes:
        thresholds[node] = random.randint(kl, ku)

    t = 1

    while True:

        new_infected = set()

        for node in remaining:
            infected_neighbors = 0
            for neighbor in G.neighbors(node):
                if neighbor in activated:
                    infected_neighbors += 1
            if infected_neighbors >= thresholds[node]:
                
                new_infected.add(node)
                activation_time[node] = t
                
                for neighbor in G.neighbors(node):
                    activation_edges.add((node,neighbor))

        if not new_infected:
            break
        
        t += 1
        remaining -= new_infected
        activated |= new_infected
    
    return activation_time

def threshold_chance(G, activated, k, p):

    remaining = set(G.nodes) - activated
    activation_edges = set()

    activation_time = defaultdict(int)

    print("Starting threshold simulation")

    t = 1

    while True:

        new_infected = set()

        for node in remaining:
            infected_neighbors = 0
            for neighbor in G.neighbors(node):
                if neighbor in activated:
                    infected_neighbors += 1
            if infected_neighbors >= k and random.random() < p:
                
                new_infected.add(node)
                activation_time[node] = t
                
                for neighbor in G.neighbors(node):
                    activation_edges.add((node,neighbor))

        if not new_infected:
            break
        
        t += 1
        remaining -= new_infected
        activated |= new_infected
    
    return activation_time

def threshold_chance_range(G, activated, kl, ku, p):

    remaining = set(G.nodes) - activated
    activation_edges = set()

    activation_time = defaultdict(int)

    print("Starting threshold simulation")

    thresholds = defaultdict(int)

    for node in G.nodes:
        thresholds[node] = random.randint(kl, ku)

    t = 1

    while True:

        new_infected = set()

        for node in remaining:
            infected_neighbors = 0
            for neighbor in G.neighbors(node):
                if neighbor in activated:
                    infected_neighbors += 1
            if infected_neighbors >= thresholds[node] and random.random() < p:
                
                new_infected.add(node)
                activation_time[node] = t
                
                for neighbor in G.neighbors(node):
                    activation_edges.add((node,neighbor))

        if not new_infected:
            break
        
        t += 1
        remaining -= new_infected
        activated |= new_infected
    
    return activation_time

def threshold_chance_range_single(G, activated, kl, ku, p):

    print("Starting threshold simulation")

    remaining = set(G.nodes) - activated
    activation_edges = set()

    activation_time = defaultdict(int)
    thresholds = defaultdict(int)
    attempted = set()

    for node in G.nodes:
        thresholds[node] = random.randint(kl, ku)

    t = 1

    while True:

        new_infected = set()

        for node in remaining:
            infected_neighbors = 0
            for neighbor in G.neighbors(node):
                if neighbor in activated:
                    infected_neighbors += 1
            if infected_neighbors >= thresholds[node]:
                attempted.add(node)
                if random.random() < p:
                    new_infected.add(node)
                    activation_time[node] = t
                    
                    for neighbor in G.neighbors(node):
                        activation_edges.add((node,neighbor))

        if not new_infected:
            break
        
        t += 1
        remaining -= attempted
        activated |= new_infected
    
    return activation_time

def moreStats(G):
    print("Number of nodes read", G.number_of_nodes())
    neighbors = [len(list(G.neighbors(node))) for node in G.nodes]
    neighbors.sort()
    print(neighbors)

    # unactivated = G.nodes - set(activated.keys())
    # print([len(list(G.neighbors(node))) for node in unactivated])



G = nx.read_edgelist("Wiki-Vote.txt", comments = "#")
moreStats(G)
seed_num = int((G.number_of_nodes() * 0.05))
print("Number of seed nodes", seed_num)
seeds = highest_degree(G, seed_num)
# seeds = coreHD(G, seed_num)
activated = threshold(G, seeds, 4)
# print(activated)
print("Total activated nodes: ", len(activated))