typedef struct grafo Grafo;

typedef struct elemento Elem;

typedef struct pilha Pilha;



Grafo* cria_Grafo(int nro_vertices, int grau_max, int eh_ponderado);
void libera_Grafo(Grafo* gr);
int insereAresta(Grafo* gr, int orig, int dest, int eh_digrafo, float peso);
Pilha* buscaProfundidade_Grafo(Grafo *gr, int ini, int *visitado);
void imprime_Grafo(Grafo *gr);


Elem* cria_lista();
void libera_lista(Elem* li);
int insere_lista(Elem* li, int valor);
void imprime_lista(Elem* li);


Pilha* pilha_cria (void);
int pilha_vazia (Pilha* p);
void pilha_push (Pilha* p, int v);
int pilha_pop (Pilha* p);
void pilha_libera (Pilha* p);
void pilha_imprime (Pilha* p);