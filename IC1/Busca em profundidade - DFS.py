INF = 9999999
# number of vertices in graph
V = 6
# create a 2d array of size 5x5
# for adjacency matrix to represent graph
G = [[0, 0, 1, 0, 0, 0],
     [0, 0, 1, 0, 1, 0],
     [1, 1, 0, 1, 1, 0],
     [0, 0, 1, 0, 1, 1],
     [0, 1, 1, 1, 0, 1],
     [0, 0, 0, 1, 1, 0]]

def adiciona(G,r,visitados,arvore,pai,nivel):
    for i in range(V):
        if G[r][i] == 1 and not visitados[i]:
            visitados[i] = True
            arvore.append((i,r,nivel+1))
            pai[i] = r
            adiciona(G,i,visitados,arvore,pai,nivel+1)
        

def DFS(G,r):
    visitados = [False] * V
    visitados[r] = True
    pilha = []
    pilha.append((r,0))
    arvore = [(r,None,0)]
    pai = [None] * V
    adiciona(G,r,visitados,arvore,pai,0)
    return arvore,pai

arvore,pai = DFS(G,2)
print(arvore)
print(pai)
                
                
        
        
    
    
    

