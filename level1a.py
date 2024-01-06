import networkx as nx
import matplotlib.pyplot as plt
import json
import scipy as sp
import numpy as np
from scipy.sparse import csr_matrix
import copy

from sys import maxsize 
from itertools import permutations


def tsp_greedy(adj, nodes):
    dense_mat = adj.todense()

    # Converting to dictionary
    sparse_dict = {}
    for i in range(dense_mat.shape[0]):
        indices = np.nonzero(dense_mat[i])[0] # get indices of non-zero elements in row i
        for j in indices:
            sparse_dict[(i, j)] = dense_mat[i, j] # use tuple (i, j) as key


    keys=(list(sparse_dict.keys()))

    temp1=keys[0]

    visited=[]
    i=0
    visited.append(nodes[i])
    visited=[]
    unvisited=copy.deepcopy(nodes)
    visited.append(unvisited[0])
    unvisited.remove(unvisited[0])
    
    print(visited)
    print(unvisited)
    curr_node=visited[0]
    for i in range(20):
        index=nodes.index(curr_node)

        print(index)
        lis={}
        for key in keys:
            if(key[0]==index):
                lis[key]=sparse_dict[key]
        print(lis)

        while True:
            minimum=min(lis.values())
            print(minimum)

            for key in lis:
                if(lis[key]==minimum):
                    min_key=key
            
            print(min_key)

            new_node_index=min_key[1]
            if(nodes[new_node_index] not in visited):
                curr_node=nodes[new_node_index]
                visited.append(curr_node)
                break
            else:
                del(lis[min_key])

    visited.append(nodes[0])
    print(visited)  
    main_dict={}

    sub_dict={}

    sub_dict["path"]=visited
    print(sub_dict)  

    main_dict["v0"]=sub_dict
    print(main_dict)

    """json_object = json.dumps(main_dict)

    with open("LEVEL_0\level1a.json", "w") as outfile:
        outfile.write(json_object)"""



f=open('LEVEL_0\level0.json')

data=json.load(f)

g=nx.Graph()

nodes=[]
nodes.append('r0')

for key in data["neighbourhoods"].keys():
    nodes.append(key)

node=nodes[0]


lis=data["restaurants"]["r0"]["neighbourhood_distance"]

j=1
for i in range(20):
    g.add_edge(node,nodes[j],weight=lis[i])
    j+=1


for i in range(1,21):
    lis=data["neighbourhoods"][nodes[i]]["distances"]
    k=0
    for j in range(1,len(lis)):
        if(nodes[i]==nodes[j]):
            continue
        g.add_edge(nodes[i],nodes[j],weight=lis[k])
        k+=1

pos = nx.shell_layout(g)

# Draw the nodes and edges
nx.draw(g, with_labels=True, node_size=1500, node_color='skyblue', font_size=10)
edge_labels = nx.get_edge_attributes(g, "weight")
nx.draw_networkx_edge_labels(g, pos, edge_labels)
# Show the plot
plt.show()



a=nx.adjacency_matrix(g, nodelist=None, dtype=None, weight='weight')

tsp_greedy(a,nodes)


