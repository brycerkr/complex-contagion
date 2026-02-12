from collections import defaultdict
import math
import random

def threshold(G, infected, k):

    activated = infected.copy()
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

def threshold_range(G, infected, kl, ku):

    activated = infected.copy()
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

def threshold_chance(G, infected, k, p):

    activated = infected.copy()
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

def threshold_chance_range(G, infected, kl, ku, p):

    activated = infected.copy()
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

def threshold_chance_range_single(G, infected, kl, ku, p):

    print("Starting threshold simulation")

    activated = infected.copy()
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

def threshold_chance_range_single_clamped(G, infected, kl, ku, p):

    infected = set(infected)
    # print("Starting threshold simulation")

    activated = infected.copy()
    remaining = set(G.nodes) - activated
    activation_edges = set()

    activation_time = defaultdict(int)
    thresholds = defaultdict(int)
    attempted = set()

    for node in G.nodes:
        thresholds[node] = min(len(list(G.neighbors(node))), random.randint(kl, ku))

    for node in G.nodes:
        if node in activated:
            activation_time[node] = 0

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

def threshold_perc(G, infected, kl, ku):

    activated = set(infected.copy())
    remaining = set(G.nodes) - activated
    
    activation_time = defaultdict(int)
    thresholds = defaultdict(int)

    for node in G.nodes:

        # Randomize threshold to round up so at least 1 neighbor is required
        # for every node to activate (important for low k)
        k = len(G.neighbors(node))
        p = random.uniform(kl,ku)
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
            for neighbor in G.neighbors(node):
                if neighbor in activated:
                    infected_neighbors += 1
            if infected_neighbors >= thresholds[node]:
                new_infected.add(node)
                activation_time[node] = t
            
        if not new_infected:
            break

        t += 1
        remaining -= new_infected
        activated |= new_infected

    return activation_time


