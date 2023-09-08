#include <stdio.h>
#include <stdlib.h>
#include "Grafo.h"
#include "insereA.h"

int main(){


    int eh_digrafo = 1;
    Grafo* gr = cria_Grafo(37, 3, 0);
    Pilha* pilha; 
    inserir(gr, eh_digrafo);
    imprime_Grafo(gr);

    printf("\n");

    int vit[37];
    pilha = buscaProfundidade_Grafo(gr, 1, vit);

    pilha_imprime(pilha);

    return 0;


    
}


























/*

    printf("\nBusca \n");
    
    int vis[37];
    printf("buscaProfundidade\n");
    buscaProfundidade_Grafo(gr, 0, vis);
    printf("fim\n");

*/