import networkx as nx
def Normelize(QX):
    sum=0
    QX2 = []
    for i in QX:
        sum += i
    # bad input:
    if sum == 0:
        return QX
    for i in range(len(QX)):
        QX2.insert(i,QX[i]/sum)
    return QX2

def Enumeration_Ask(X,e,bn):
    QX = [0,0]
    for i in [0,1]:
        e[X]=i
        QX[i]=Enumerate_All(list(nx.topological_sort(bn.dirgraph)),e.copy(),bn)
    return Normelize(QX)

def Enumerate_All(vars,e,bn):
    if len(vars) == 0:
        return 1
    y = vars.pop(0)
    if y in e.keys():
        p = bn.get_bayesPr(y, e.copy())
        return p*Enumerate_All(vars.copy(), e.copy(), bn)
    else:
        sum = 0
        for i in [0,1]:
            e[y] = i
            p1 = bn.get_bayesPr(y,e.copy())
            sum += p1*Enumerate_All(vars.copy(), e.copy(), bn)
        return sum