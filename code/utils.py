import os
import pickle
import networkx as nx
import numpy as np

def load_graph(fn):
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

def load_pickle_file(file_path):
    with open(file_path, 'rb') as file:
        return pickle.load(file)

def save_pickle_file(file_path, data):
    with open(file_path, 'wb') as file:
        pickle.dump(data, file)

def for_each_file(base_dir, func):
    for root, dirs, files in os.walk(base_dir):
        for dir_name in dirs:
            sub_dir = os.path.join(root, dir_name)
            if not any(os.path.isdir(os.path.join(sub_dir, name)) for name in os.listdir(sub_dir)):
                func()

metadata = {
    "threshold_distribution" : "",
    "mean" : "",
    "standard_deviation" : "",
    "model" : "",
    "fIA" : "",
    "avg_cascade_size" : ""
}

