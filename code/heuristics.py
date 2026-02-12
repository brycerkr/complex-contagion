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

def degree_discount(G,seeds,p_infection):
    # initializse stuff
    seed_nodes = set()
    dd_v = dict(G.degree())
    t_v = dict([(n,0) for n in G.nodes()])

    # select nodes
    for i in range(seeds):
        k_max = max([k for n,k in dd_v.items() if n not in seed_nodes])
        # randomly select one node that has k = k_max
        node = random.choice([n for n,k in dd_v.items() if (k == k_max) and (n not in seed_nodes)])
        seed_nodes.add(node)

        # compute t_v abnd update dd_v
        for neigh in G.neighbors(node):
            t_v[neigh] += 1

            d = G.degree(neigh)
            t = t_v[neigh]

            dd_v[neigh] = d - 2*t - (d-t)*t*p_infection
    return list(seed_nodes)

def coreHD(G,seeds):
    H = G.copy().copy()
    H.remove_edges_from(nx.selfloop_edges(H))
    seed_nodes = []
    for i in range(seeds):
        # find k=2 core
        kcore = nx.k_core(H, k=2)

        # find node or nodes with max degree node
        k_max = max(dict(kcore.degree()).values())

        # if mode candidates pick random node
        node = random.choice([n for n, k in dict(kcore.degree()).items() if k == k_max])

        H.remove_node(node)
        seed_nodes.append(node)

    return seed_nodes

def random_selection(G, seeds):
    seed_nodes = random.sample(sorted(G.nodes), seeds)
    return seed_nodes

def acquaintance(G, seeds):
    random_nodes = random_selection(G, seeds)
    seed_nodes = set()

    for node in random_nodes:
        seed_nodes.add(random.sample(G.neighbors(node),1))
    
    return seed_nodes