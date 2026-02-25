import networkx as nx
import numpy as np

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