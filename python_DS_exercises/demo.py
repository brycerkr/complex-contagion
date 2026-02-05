from collections import defaultdict
import random
from matplotlib import animation
import matplotlib.pyplot as plt
import networkx as nx

def highest_degree(G, seed_num):
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

def ICM(G, infected, p_infection):

    activated = infected.copy()
    activation_time = defaultdict(int)

    # add initial seed to activated & activation_time
    for n in infected:
        activation_time[n] = 0

    t = 1
    # run infection process
    while infected != set():
        new_infected = set()
        activation_edges = set()
        
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

def main():
    n = 200    #Size of network


    m = 2      #Min. degree for B-A
    o = 0.05    #Edge p for E-R

    seed_size = 4      #Size of seeded set
    p_infection = 0.15  #Transmission probability -- good values are 0.3 for B-A and 0.15 for E-R


    #SF = nx.barabasi_albert_graph(n,m)

    SF = nx.erdos_renyi_graph(n, o)

    #pos = nx.kamada_kawai_layout(SF)
    pos = nx.spring_layout(SF, k=1.4, iterations=600)

    seed_nodes = highest_degree(SF, seed_size)

    frames = list(ICM(SF, seed_nodes, p_infection))

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
        edge_color="lightgray",
        alpha=0.2,
        width=3.0,
        ax=ax
    )

    activated_edges = set()

    def init():
        state = frames[0]
        
        colors = [
            "red" if n in state["active"] else "lightblue"
            for n in SF.nodes()
        ]

        nodes.set_color(colors)
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

if __name__ == "__main__":
    main()
