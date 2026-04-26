import networkx as nx
from utils import load_graph
import matplotlib.pyplot as plt

G = load_graph("datasets_ignored/village.csv")

isolates = nx.isolates(G)
G.remove_nodes_from(list(isolates))

# Generate 3D positions
pos = nx.spring_layout(G, dim=3)

# Extract node positions
x = [pos[n][0] for n in G.nodes()]
y = [pos[n][1] for n in G.nodes()]
z = [pos[n][2] for n in G.nodes()]

# Create 3D plot
fig = plt.figure(figsize=(10,10))
ax = fig.add_subplot(111, projection='3d')

# Draw nodes
ax.scatter(x, y, z)

# Draw edges
for edge in G.edges():
    x_coords = [pos[edge[0]][0], pos[edge[1]][0]]
    y_coords = [pos[edge[0]][1], pos[edge[1]][1]]
    z_coords = [pos[edge[0]][2], pos[edge[1]][2]]
    ax.plot(x_coords, y_coords, z_coords, alpha=0.2)

plt.show()