import networkx as nx
import matplotlib.pyplot as plt
import json
import scipy as sp

from sys import maxsize 
from itertools import permutations

f=open('LEVEL_0\level0.json')

data=json.load(f)

g=nx.Graph()

nodes=[]
nodes.append('r0')

for key in data["neighbourhoods"].keys():
    nodes.append(key)

#print(nodes)

node=nodes[0]
print(nodes)

lis=data["restaurants"]["r0"]["neighbourhood_distance"]

j=1
for i in range(20):
    g.add_edge(node,nodes[j],weight=lis[i])
    j+=1


print(g.edges())

for i in range(1,21):
    lis=data["neighbourhoods"][nodes[i]]["distances"]
    #print(len(lis))
    #print(lis)
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


print(len(g.edges()))

for node in g.nodes():
    print(list(g.neighbors(node)))


a=nx.adjacency_matrix(g, nodelist=None, dtype=None, weight='weight')
adj=a.todense()

#print(adj)
#print(type(adj))

adj_list=adj.tolist()
print(adj_list)
print(type(adj_list))












