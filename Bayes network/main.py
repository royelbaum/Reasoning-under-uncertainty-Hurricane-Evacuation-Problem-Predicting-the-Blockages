
from Graph import *
from BayesNetwork import *
from Enumaration import Enumeration_Ask

def convert_Path(path,t,graph):
    p=[]
    for i in range(len(path)-1):
        p=p+[graph.edges[path[i],path[i+1]]["name"]]
    return list(map(lambda x: "E" + str(x) + "t= " + str(t), p))

def path_non_blocked_Pr(path,E,bn,t):
    p=convert_Path(path,t,bn.graph)
    pr=1
    for e in p:
        en=Enumeration_Ask(e,E,bn)
        pr=pr*en[0]

        E[e]=0
    return pr

def bestPath(v1,v2,bn,t,E):
    paths=list(nx.all_simple_paths(bn.graph, source=v1, target=v2))
    pr=0
    best_P=[]
    for p in paths:
        tmp=path_non_blocked_Pr(p,E.copy(),bn,t)
        if tmp>pr:
            pr=tmp
            best_P=p
    return [best_P,pr]


graph = nx.Graph()
p=make_graph("graph.txt",graph)


BN=BayesNet(graph,p,1)

print("the path with the best chance of not being blocked between nodes 1 and 3 is:\twith probability:\n\t",
      bestPath(1, 3, BN, 1, {"E2t= 0":1,"2":0}))
print("pr(vertex 2 Evacuation |e2 is blocked in t=0)= ",Enumeration_Ask("2",{"E2t= 0":1},BN))
print("pr(e2 blockage in t=1 |vertex 2 Evacuees)= ",Enumeration_Ask("E2t= 1",{"2":1},BN))
print("pr(e2 blockage in t=0 |vertex 2 Evacuees)= ",Enumeration_Ask("E2t= 0",{"2":1},BN))
print("pr(e2 blockage in t=1 |vertex 2 Evacuees)= ",Enumeration_Ask("E2t= 1",{"2":0},BN))
print("pr(e2 blockage in t=0 |vertex 2 Evacuees)= ",Enumeration_Ask("E2t= 0",{"2":0},BN))
print(Enumeration_Ask("E3t= 0",{"2":1,"E3t= 1":1},BN))
draw_g_dir(BN.dirgraph)