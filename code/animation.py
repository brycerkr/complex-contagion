from collections import Counter, defaultdict
import random
from matplotlib import pyplot as plt
import networkx as nx
import numpy as np
from heuristics import highest_degree, coreHD



def ICM_gen(G, infected, p_infection):

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

def threshold_gen(G, infected, k):

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

def anim_demo():
    """
    Demo of animation for infection spreading
    Has a few glitches
    Works best for a few 100 nodes max
    """

    n = 400    #Size of network

    m = 2      #Min. degree for B-A
    o = 0.05    #Edge p for E-R

    seed_size = 80      #Size of seeded set
    p_infection = 0.3  #Transmission probability -- good values are 0.3 for B-A and 0.15 for E-R


    SF = nx.barabasi_albert_graph(n,m)
    #SF = nx.erdos_renyi_graph(n, o)

    #pos = nx.kamada_kawai_layout(SF)
    pos = nx.spring_layout(SF, k=1.4, iterations=600)

    seed_nodes = highest_degree(SF, seed_size)

    frames = list(ICM_gen(SF, seed_nodes, p_infection))
    # frames = list(threshold(SF, seed_nodes, 2))

    fig, ax = plt.subplots()

    nodes = nx.draw_networkx_nodes(
        SF, pos,
        node_size=80,
        node_color="lightblue",
        ax=ax
    )

    edges = nx.draw_networkx_edges(
        SF,
        pos,
        arrows=False,
        edge_color="lightgray",
        alpha=0.2,
        width=3.0,
        ax=ax
    )

    activated_edges = set()

    def init():
        state = frames[0]
        
        node_colors = [
            "red" if n in state["active"] else "lightblue"
            for n in SF.nodes()
        ]

        edge_colors = [
            "red" if e in state["edges"] else "lightgray"
            for e in SF.edges()
        ]

        nodes.set_color(node_colors)
        edges.set_color(edge_colors)

        ax.set_title("t = 0")

        return nodes,

    def update(i):
        state = frames[i]
        activated_edges.update(state["edges"])

        active = state["active"]
        new = state["new"]

        active = state["active"]

        colors = []
        for n in SF.nodes():
            if n in new:
                colors.append("orange")
            elif n in active:
                colors.append("red")
            else:
                colors.append("lightblue")
        nodes.set_color(colors)

        edge_alphas = []
        edge_colors = []
        for u, v in SF.edges():
            if (u, v) in activated_edges or (v, u) in activated_edges:
                edge_alphas.append(0.5)
                edge_colors.append("red")
            else:
                edge_alphas.append(0.2)
                edge_colors.append("lightgray")
        edges.set_alpha(edge_alphas)
        edges.set_color(edge_colors)

        ax.set_title(f"t = {state['t']}")

        return nodes, edges

    ax.set_axis_off()

    ani = animation.FuncAnimation(
        fig,
        update,
        frames=len(frames),
        init_func=init,
        interval=1500,
        blit=True,
        cache_frame_data=False
    )

    plt.show()