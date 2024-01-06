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
    
    #print(visited)
    #print(unvisited)
    curr_node=visited[0]
    for i in range(20):
        index=nodes.index(curr_node)

        #print(index)
        lis={}
        for key in keys:
            if(key[0]==index):
                lis[key]=sparse_dict[key]
        #print(lis)

        while True:
            minimum=min(lis.values())
            #print(minimum)

            for key in lis:
                if(lis[key]==minimum):
                    min_key=key
            
            #print(min_key)

            new_node_index=min_key[1]
            if(nodes[new_node_index] not in visited):
                curr_node=nodes[new_node_index]
                visited.append(curr_node)
                break
            else:
                del(lis[min_key])

    visited.append(nodes[0])
    #print(visited)  
    main_dict={}

    sub_dict={}

    sub_dict["path"]=visited
    #print(sub_dict)  

    main_dict["v0"]=sub_dict
    #print(main_dict)

    """json_object = json.dumps(main_dict)

    with open("LEVEL_0\level1a.json", "w") as outfile:
        outfile.write(json_object)"""
    return main_dict,sparse_dict


def find_slots(veh_tot_capacity_dict,path_list,edge_weight_dict,nodes,node_qty):

    start_node=nodes[0]
    veh_tot_capacity=list(veh_tot_capacity_dict.values())
    curr_node=start_node
    visited=[]
    tot_paths=[]
    new_ew_dict={}
    for key in edge_weight_dict.keys():
        if(key[1]==0):
            continue
        else:
            new_ew_dict[key]=edge_weight_dict[key]

    keys=list(new_ew_dict.keys())

    #print(new_ew_dict)
    fill=0
    curr_node=start_node
    
    visited.append(curr_node)
    tot_paths=[]
    count=0
    i=0
    while(len(visited)<21):
        count+=1
        curr_node=start_node
        fill=0
        path=[]
        path.append("r0")
        print("\n\ncurr node:",curr_node)
        while(fill<=veh_tot_capacity[i]):
            flag=0
            lis={}
            index=nodes.index(curr_node)
            for key in keys:
                if(key[0]==index):
                    lis[key]=new_ew_dict[key]
            #print("list:",lis)
            while(True):
                #print("len:" , len(lis.values()))
                min_val=min(lis.values())
                #key_lis=list(lis.keys())
                for key in lis:
                    if(new_ew_dict[key]==min_val):
                        min_key=key
                new_node=min_key[1]
                if(nodes[new_node] not  in visited):
                    #print("went inside")
                    temp_curr_node=nodes[new_node]
                    fill+=node_qty[temp_curr_node]
                    if(fill>veh_tot_capacity[i]):
                        flag=1
                        break
                    curr_node=nodes[new_node]
                    print("fill: ",fill)
                    visited.append(curr_node)
                    path.append(curr_node)
                    break
                else:
                    #print("visited:",visited)
                    #print("Already in visited: ",nodes[min_key[1]])
                    del(lis[min_key])
                    continue
            if(flag==1):
                continue
            #print("min_node_out:",nodes[new_node])
            print("\n\npath:", path)
            print('len: ',len(visited))

            
            if(fill>veh_tot_capacity[i]):
                break
            if(len(visited)==21):
                break

        print("visited: ",visited)    
        if(count%2==0):
            i+=1
        tot_paths.append(path)

    
    #print(tot_paths)

    for path in tot_paths:
        path.append("r0")

    print(tot_paths)

    print(len(tot_paths))

    subdict={}
    subdict1={}
    subdict1["path1"]=tot_paths[0]
    subdict1["path2"]=tot_paths[1]
    subdict["v0"]=subdict1

    subdict2={}
    subdict2["path1"]=tot_paths[2]
    subdict2["path2"]=tot_paths[3]
    subdict["v1"]=subdict2

    subdict3={}
    subdict3["path1"]=tot_paths[4]
    subdict3["path2"]=tot_paths[5]
    subdict["v2"]=subdict3

    subdict4={}
    subdict4["path1"]=tot_paths[6]
    subdict["v3"]=subdict4

    print(subdict)







    json_object = json.dumps(subdict)

    with open("LEVEL_0\level2a_output.json", "w") as outfile:
        outfile.write(json_object)

   


f=open('LEVEL_0\level2a.json')

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

tsp_path_dict,edge_weight_dict=tsp_greedy(a,nodes) 

path_list=tsp_path_dict["v0"]["path"]

tot_qty={}
for vehicle in data["vehicles"].keys():
    tot_qty[vehicle]=data["vehicles"][vehicle]["capacity"]
print(tot_qty)

print(path_list)

node_qty={}

for i in range(1,len(nodes)):
    node_qty[nodes[i]]=data["neighbourhoods"][nodes[i]]["order_quantity"]

print(node_qty)


find_slots(tot_qty,path_list,edge_weight_dict,nodes,node_qty)



