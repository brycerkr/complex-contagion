from collections import defaultdict
import random


def ICM(G, infected, p_infection):

    activated = infected.copy()
    activation_edges = set()
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
                    activation_edges.add((node,neighbor))

        yield {
            "t": t,
            "active": activated.copy(),
            "new": new_infected.copy(),
            "edges": activation_edges.copy(),
        }

        # set of newly infected nodes
        infected = new_infected.copy()

        # update time counter
        t += 1

    # return list of infected/recovered nodes
    # return activation_time

def threshold(G, infected, k):

    remaining = set(G.nodes) - infected
    activated = infected.copy()
    new_infected = remaining.copy()
    activation_edges = set()

    print("Starting threshold simulation")

    t = 1

    while True:

        new_infected = set()

        for node in remaining:
            infected_neighbors = 0
            for neighbor in G.neighbors(node):
                if neighbor in infected:
                    infected_neighbors += 1
            if infected_neighbors > k:
                
                new_infected.add(node)
                
                for neighbor in G.neighbors(node):
                    activation_edges.add((node,neighbor))

        if not new_infected:
            break
        
        remaining -= new_infected
        activated |= new_infected

        yield {
            "t": t,
            "active": activated.copy(),
            "new": new_infected.copy(),
            "edges": activation_edges.copy()
        }

