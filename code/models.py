from collections import defaultdict
import math
import random
from scipy.stats import truncnorm
from typing import Any

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

def threshold(G, infected, kl, ku) -> defaultdict[Any, int]:
    """
    Implementation of a threshold model for information cascade simulation.
    Threshold uniformly sampled between a lower and an upper bound.
    
    :param G: Graph
    :param infected: Initial set of infected nodes in G
    :param kl: Lower bound of threshold probability
    :param ku: Upper bound of threshold probability
    :return: A mapping of activated nodes to the timestep in which they were activated
    :rtype: defaultdict[Any, int]
    """

    activated = set(infected.copy())
    remaining = set(G.nodes) - activated
    
    activation_time = defaultdict(int)
    thresholds = defaultdict(int)

    for node in G.nodes:

        # Randomize threshold to round up so at least 1 neighbor is required
        # for every node to activate (important for low k)
        k = len(list(G.neighbors(node)))
        p = random.uniform(kl,ku)
        # print(f"Sampled {p}")
        thresholds[node] = math.ceil(k * p)

        # Seed nodes activated in timestep 0
        if node in activated:
            activation_time[node] = 0

    # Start timestep at 1
    t = 1

    while True:

        new_infected = set()

        for node in remaining:
            infected_neighbors = 0

            # Count activated neighbors
            for neighbor in G.neighbors(node):
                if neighbor in activated:
                    infected_neighbors += 1
            if infected_neighbors >= thresholds[node]:
                new_infected.add(node)
                activation_time[node] = t
            
        if not new_infected:
            break

        # Discrete timesteps, remaining and activated only mutated once per round
        t += 1
        remaining -= new_infected
        activated |= new_infected

    return activation_time

def threshold_norm(G, infected, mean_threshold, threshold_std) -> defaultdict[Any, int]:
    """
    Implementation of a threshold model for information cascade simulation.
    Threshold sampled from a normal distribution.
    :param G: Graph
    :param infected: Initial set of infected nodes in G
    :param mean_threshold: The mean thresholde 
    :param threshold_std: The standard deviation
    :return: A mapping of activated nodes to the timestep in which they were activated
    :rtype: defaultdict[Any, int]
    """

    # Prepare thresholds
    ps = truncnorm_thresholds(len(G.nodes()), mean_threshold, threshold_std)
    thresholds = apply_thresholds(G, ps)
    
    activation_time = defaultdict(int)

    # Activate seed nodes in timestep 0
    for node in G.nodes():
        if node in infected:
            activation_time[node] = 0

    # Start timestep at 1
    t = 1

    # Initialize activated and remaining sets
    activated = set(infected.copy())
    remaining = set(G.nodes) - activated

    while True:

        new_infected = set()

        for node in remaining:
            infected_neighbors = 0

            # Count activated neighbors
            for neighbor in G.neighbors(node):
                if neighbor in activated:
                    infected_neighbors += 1
            if infected_neighbors >= thresholds[node]:
                new_infected.add(node)
                activation_time[node] = t
            
        if not new_infected:
            break

        # Discrete timesteps, remaining and activated only mutated once per round
        t += 1
        remaining -= new_infected
        activated |= new_infected

    return activation_time

def threshold_norm_special(G, infected, mean_threshold, threshold_std):
    """
    Implementation of a threshold model for information cascade simulation.
    Threshold sampled from a normal distribution.
    :param G: Graph
    :param infected: Initial set of infected nodes in G
    :param mean_threshold: The mean thresholde 
    :param threshold_std: The standard deviation
    :return: A mapping of activated nodes to the timestep in which they were activated
    :rtype: defaultdict[Any, int]
    """

    # Prepare thresholds
    ps = truncnorm_thresholds(len(G.nodes()), mean_threshold, threshold_std)
    thresholds = apply_thresholds(G, ps)
    
    activation_time = defaultdict(int)

    # Activate seed nodes in timestep 0
    for node in G.nodes():
        if node in infected:
            activation_time[node] = 0

    # Start timestep at 1
    t = 1

    # Initialize activated and remaining sets
    activated = set(infected.copy())
    remaining = set(G.nodes) - activated

    while True:

        new_infected = set()

        for node in remaining:
            infected_neighbors = 0

            # Count activated neighbors
            for neighbor in G.neighbors(node):
                if neighbor in activated:
                    infected_neighbors += 1
            if infected_neighbors >= thresholds[node]:
                new_infected.add(node)
            
        if not new_infected:
            break

        # Discrete timesteps, remaining and activated only mutated once per round
        t += 1
        remaining -= new_infected
        activated |= new_infected

    return activated

def truncnorm_thresholds(size, mean_threshold, threshold_std):

    lower, upper = 0, 1     # Abscissae of truncated normal distribution

    # Calculate abscissae in standard deviations from mean for truncnorm function
    lower_bound = (lower - mean_threshold) / threshold_std
    upper_bound = (upper - mean_threshold) / threshold_std

    return truncnorm.rvs(lower_bound, upper_bound, loc=mean_threshold, scale=threshold_std, size=size)

def uniform_thresholds(size, lower, upper):
    ps = []

    for _ in range(size):
        ps.append(random.uniform(lower,upper))
    
    return ps

def apply_thresholds(G, ps):

    thresholds = defaultdict(int)

    for node, p in zip(G.nodes, ps):
        k = G.degree[node]                         # Get degree of node
        thres = math.ceil(k * p)                   # Ceiling to whole number
        thresholds[node] = max(1, thres)      # Because theoretically truncnorm can sample 0 

    return thresholds 
      