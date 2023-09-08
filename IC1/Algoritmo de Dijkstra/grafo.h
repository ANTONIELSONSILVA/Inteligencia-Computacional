    struct adjacencia{
        int peso;
        int vertices;
        int destino;
        struct adjacencia *prox;
    };
    typedef struct adjacencia ADJACENCIA;


   struct adj{

        ADJACENCIA *cab;

    };
    typedef struct adj ADJ;


    struct grafo{
        int vertices;   
        ADJ *adj;
    };
    typedef struct grafo Grafo;


Grafo *criaGrafo(int vertices);

void criaAresta(Grafo* gr, int vertices, int destino, int peso);

void imprimirGrafo(Grafo *gr);

void inicializaD(Grafo *g, int *d , int *p, int s);

void relaxa(Grafo *g, int *d, int *p, int u, int v);

//bool existeAberto(Grafo *g, int *aberto);
int existeAberto(Grafo *g, int *aberto);

int menorDist(Grafo *g, int *aberto, int *d);

int *dijkstra(Grafo *g, int s);

void grafo_imprime(Grafo* gr);