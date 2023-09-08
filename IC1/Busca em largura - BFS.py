INF = 9999999
# number of vertices in graph
V = 6
# create a 2d array of size 5x5
# for adjacency matrix to represent graph
G = [[0, 1, 1, 0, 0, 0],
     [1, 0, 1, 1, 1, 0],
     [1, 1, 0, 1, 1, 0],
     [0, 1, 1, 0, 1, 1],
     [0, 1, 1, 1, 0, 1],
     [0, 0, 0, 1, 1, 0]]

def BFS(G,r):
    visitados = [False] * V
    visitados[r] = True
    fila = []
    fila.append((r,0))
    arvore = [(r,None,0)]
    pai = [None] * V
    while len(fila)>0:
        atual = fila.pop(0)
        for i in range(V):
            if G[atual[0]][i] == 1 and not visitados[i]:
                visitados[i] = True
                fila.append((i,atual[1]+1))
                arvore.append((i,atual[0],atual[1]+1))
                pai[i] = atual[0]
    return arvore,pai

arvore,pai = BFS(G,0)
print(arvore)
print(pai)
                
                
        
        
    
    
    