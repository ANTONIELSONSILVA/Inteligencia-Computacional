#include <stdio.h>
#include <stdlib.h>
#include <limits.h>
#include "grafo.h"


Grafo* criaGrafo(int vertices){

    Grafo* novoG = (Grafo*) malloc(sizeof(Grafo));
    ADJ* novoA = (ADJ*) malloc(vertices * sizeof(ADJ));

    novoG->vertices = vertices;
    novoG->adj = novoA;

    for (int i = 0; i <= vertices; i++)
    {
        novoG->adj[i].cab = NULL;
    }

    return novoG;

}


void criaAresta(Grafo* gr, int vertices, int destino, int peso){
    
    ADJACENCIA *Aux=NULL;

    if (gr->adj[vertices].cab == NULL){
        Aux = (ADJACENCIA*) malloc(sizeof(ADJACENCIA));
        Aux->prox = NULL;
        Aux->destino = destino;
        Aux->peso = peso;
        gr->adj[vertices].cab = Aux;

    }else{

        Aux = gr->adj[vertices].cab;

        while(Aux->prox != NULL){
            Aux = Aux->prox;
        }

        ADJACENCIA* novo = (ADJACENCIA*) malloc(sizeof(ADJACENCIA));
        novo->prox = NULL;
        Aux->destino = destino;
        Aux->peso = peso;

        Aux->prox = novo;

    }

}



void imprimirGrafo(Grafo *gr){

    ADJACENCIA *Aux;

    for(int i = 0; i <= gr->vertices; i++){
        
        Aux = gr->adj[i].cab;

        while(Aux->prox != NULL){
            printf("Vertice: V %i Destino: U %i Peso: %i \n\n", i, Aux->destino, Aux->peso);
            Aux = Aux->prox;
        }

    }


}


void inicializaD(Grafo *g, int *d , int *p, int s){

    // int *d - vetor de distâncias, int *p - predecessores
    // g->vertives, provavelmento o N° vertices

    for (int v = 0; v < g->vertices; ++v){
        d[v] = INT_MAX/2;     // distancia infinito limits.h
        p[v] = -1;			  //
    }


    // s vindo com como paramentro da função representa o vertice inicial
    // setado com 0 vai sr o menor o portanto o inicial

    d[s] = 0;  

}

                                       // Aresta de U a V
void relaxa(Grafo *g, int *d, int *p, int u, int v){

    ADJACENCIA *ad = g->adj[u].cab;
    while(ad && ad->vertices != v)
        ad = ad->prox;

    if(ad){

        if(d[v] > d[u] + ad->peso){

            d[v] = d [u] + ad->peso;
            p[v] = u;

        }
    }

}



int existeAberto(Grafo *g, int *aberto){

    for (int i = 0; i < g->vertices; ++i)
    {
        if (aberto[i])
        {
            return(1);
        }
    }

    return(0);
}



int menorDist(Grafo *g, int *aberto, int *d){

    int i;
    for (i = 0; i < g->vertices; i++){

        if (aberto[i]==1){
            break;
        }

    }

    if (i == g->vertices){
        return(-1);
    }

    int menor = i;

    for (i = menor + 1; i < g->vertices; i++){
        if (aberto[i] == 0 && (d[menor]>d[i])){
            menor = i;
        }
    }

    return (menor);

}



int *dijkstra(Grafo *g, int s){

    // int *d - vetor de distâncias.
    int* d = (int*) malloc(g->vertices * sizeof(int));

    // int *p - predecessores
    int p[g->vertices];

    int aberto[g->vertices];

    // g - grafo, d - distancias, p -predecessores, s-vetor inicial 
    inicializaD(g,d,p,s);

    // todos os vertices estã abertos, não foram visitados.
    for (int i = 0; i < g->vertices; ++i)
        aberto[i] = 1;


    while(existeAberto(g, aberto)){

        int u = menorDist(g, aberto, d);
        aberto[u] = 0;

        ADJACENCIA *ad = g->adj[u].cab;   // lista ligada

        while(ad){

           // void relaxa(Grafo *g, int *d, int *p, int u, int v){
            relaxa(g,d,p,u,ad->vertices);
            ad = ad->prox;
        
        }
    }

    return(d);

}


void grafo_imprime(Grafo* gr){

    Grafo* Aux = gr;
    ADJACENCIA* adj;

    for(int i = 0; i <= gr->vertices; i++){
        adj = gr->adj[i].cab;

        for (adj ; adj->prox != NULL ; adj = adj->prox)
        {
            printf("Vertice: %i -- Aresta: %i -- Peso: %i \n", i, adj->destino, adj->peso);
        }

    }

}