import networkx as nx


class BayesNet(object):
    def __init__(self, graph, persistence, t):
        self.graph = graph
        self.Ppersistence = persistence
        self.ByesPr = {}
        self.dirgraph = nx.DiGraph()
        self.createBayesNet(t)

    def createBayesNet(self, t):
        i = 0
        for v in self.graph.nodes:
            self.ByesPr[str(v)] = [1 - self.graph.nodes[v]["P"], self.graph.nodes[v]["P"]]
            self.dirgraph.add_node(str(v), P=self.graph.nodes[v]["P"], VERTEX=True)
        for e in self.graph.edges:
            b2 = self.P_E_block(e, False, False)
            b1 = self.P_E_block(e, False, True)
            b0 = self.P_E_block(e, True, True)
            self.ByesPr[(e, 0)] = [b0, b1, b2]

            ename = "E" + self.graph.edges[e]["name"] + "t= " + str(i)

            self.dirgraph.add_node(ename, V1=e[0], V2=e[1], T=0, VERTEX=False)
            self.dirgraph.add_edge(str(e[0]), ename)
            self.dirgraph.add_edge(str(e[1]), ename)

        while t > 0:
            t = t - 1
            i += 1
            for e in self.graph.edges:
                self.ByesPr[(e, i)] = [0.001, self.Ppersistence]
                old_t_name = "E" + self.graph.edges[e]["name"] + "t= " + str(i - 1)
                ename = "E" + self.graph.edges[e]["name"] + "t= " + str(i)
                self.dirgraph.add_node(ename, V1=e[0], V2=e[1], T=i, VERTEX=False)
                self.dirgraph.add_edge(old_t_name, ename)

    def P_E_block(self, e, e0, e1):
        if e0:
            if e1:
                return 0.001
            else:
                return self.pi(e)
        elif e1:
            return self.pi(e)

        return 1 - pow((1 - self.pi(e)), 2)

    def pi(self, e):
        return (1 / float(self.graph.edges[e]["weight"])) * 0.6


    def get_bayesPr (self, x, e):
        if self.dirgraph.nodes[x]["VERTEX"]:
            if e[x] == 1:
                return self.dirgraph.nodes[x]["P"]
            else:
                return 1 - self.dirgraph.nodes[x]["P"]

        t = int(self.dirgraph.nodes[x]["T"])
        v1 = int(self.dirgraph.nodes[x]["V1"])
        v2 = int(self.dirgraph.nodes[x]["V2"])
        if t == 0:
            p = self.ByesPr[((v1, v2), t)][e[str(v1)] + e[str(v2)]]
        else:
            parent_name = "E" + self.graph.edges[(v1, v2)]["name"] + "t= " + str(t - 1)
            p = self.ByesPr[((v1, v2), t)][e[parent_name]]
        if x in e.keys():
            if e[x] == 0:
                return 1 - p
        return p
