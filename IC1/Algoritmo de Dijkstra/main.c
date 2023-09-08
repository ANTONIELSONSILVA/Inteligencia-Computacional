#include <stdio.h>
#include <stdlib.h>
#include "grafo.h"


int main()
{
    Grafo *gr = criaGrafo(6);
    Grafo *Aux = gr;
    criaAresta(gr, 0, 1, 10);
    criaAresta(gr, 0, 2, 5);
    criaAresta(gr, 1, 3, 1);
    criaAresta(gr, 2, 1, 3);
    criaAresta(gr, 2, 4, 2);
    criaAresta(gr, 2, 3, 8);
    criaAresta(gr, 3, 5, 4);
    criaAresta(gr, 3, 4, 4);
    criaAresta(gr, 4, 5, 6);

    int *r = dijkstra(gr, 0);
    for (int i = 0; i < gr->vertices; ++i)
         printf("D(v0 -> v%d) = %d\n", i,r[i]) ;

    return 0;

}



































/*

    ADJACENCIA *A;

    A = gr->adj[0].cab;
    printf("Destino: %i -- Peso: %i \n", A->destino, A->peso);

    A = gr->adj[1].cab;
    printf("Destino: %i -- Peso: %i \n", A->destino, A->peso);

    A = gr->adj[2].cab;
    printf("Destino: %i -- Peso: %i \n", A->destino, A->peso);

    A = gr->adj[3].cab;
    printf("Destino: %i -- Peso: %i \n", A->destino, A->peso);

    A = gr->adj[4].cab;
    printf("Destino: %i -- Peso: %i \n", A->destino, A->peso);


    imprimirGrafo(gr);

























    struct adjacencia{
        int peso;
        int vertices;
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
















    */