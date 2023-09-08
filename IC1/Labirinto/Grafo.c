#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "Grafo.h"

//Definição do tipo Grafo
struct grafo{

    int eh_ponderado;
    int nro_vertices;
    int grau_max;
    int** arestas;
    float** pesos;
    int* grau;
};

typedef struct elemento{
    int valor;
    struct elemento* prox;
}Elem;


typedef struct pilha{
    Elem* prim;
}Pilha;


//====================  CRIAR ESTRUTURAS ======================

Grafo* cria_Grafo(int nro_vertices, int grau_max, int eh_ponderado){
    Grafo *gr;
    gr = (Grafo*) malloc(sizeof(struct grafo));
    if(gr != NULL){
        int i;
        gr->nro_vertices = nro_vertices;
        gr->grau_max = grau_max;
        gr->eh_ponderado = (eh_ponderado != 0)?1:0;
        gr->grau = (int*) calloc(nro_vertices,sizeof(int));

        gr->arestas = (int**) malloc(nro_vertices * sizeof(int*));
        for(i=0; i<nro_vertices; i++)
            gr->arestas[i] = (int*) malloc(grau_max * sizeof(int));

    }
    return gr;
}



Pilha* pilha_cria (void)
{
    Pilha *p = (Pilha*) malloc(sizeof(Pilha));
    p->prim = NULL;
    return p;
}



Elem* cria_lista(){

    Elem* li = (Elem*) malloc(sizeof(Elem));
    return li;
}



int insereAresta(Grafo* gr, int orig, int dest, int eh_digrafo, float peso){
    if(gr == NULL){
        return 0;
    }


    gr->arestas[orig][gr->grau[orig]] = dest;
    gr->grau[orig]++;

    if(eh_digrafo == 0)
        insereAresta(gr,dest,orig,1,peso);
    return 1;


}


int pilha_vazia (Pilha* p)
{
    if(p->prim == NULL)
        return 1;
    return 0;
}


int insere_lista(Elem* li, int valor){

    if(li == NULL){
        return 0;
    }


    Elem *no;
    no = (Elem*) malloc(sizeof(Elem));
    

    if(no == NULL)
        return 0;
    no->valor = valor;
    no->prox = NULL;
    if(li == NULL){//lista vazia: insere início
        li = no;
    }else{
        Elem *aux;
        aux = li;
        while(aux->prox != NULL){
            aux = aux->prox;
        }
        aux->prox = no;
    }

    return 1;

}


int pilha_pop (Pilha* p)
{
    Elem *t;
    int v;

    if (pilha_vazia(p)){
        printf("Pilha vazia.\n");
        return 0;
    }

    t = p->prim;
    v = t->valor;
    p->prim = t->prox;
    free(t);
    return v;

}


void pilha_push (Pilha* p, int v)
{
    Elem *novo;
    novo = (Elem*) malloc(sizeof(Elem));
    novo->valor = v;
    novo->prox = p->prim;
    p->prim = novo;

}


//==============  IMPRIMIR ESTRUTURAS ======================



void imprime_Grafo(Grafo *gr){
    if(gr == NULL)
        return;

    int i, j;
    for(i=0; i < gr->nro_vertices; i++){
        printf("%d: ", i);
        for(j=0; j < gr->grau[i]; j++){
            if(gr->eh_ponderado)
                printf("%d(%.2f), ", gr->arestas[i][j], gr->pesos[i][j]);
            else
                printf("%d, ", gr->arestas[i][j]);
        }
        printf("\n");
    }
}

void pilha_imprime (Pilha* p){

    Elem *q = p->prim, *t;

    while(q != NULL)
    {
        t = q->prox;
        printf("%i\n", t->valor );
        q = t;
    }

}



void imprime_lista(Elem* li){

    if(li == NULL){
        return;
    }

    Elem* no = li;
    while(no != NULL){
       printf("%i \n", no->valor);
        no = no->prox;
    }
}


//==============  LIBERAR ESTRUTURAS ======================

void libera_Grafo(Grafo* gr){
    if(gr != NULL){
        int i;
        for(i=0; i<gr->nro_vertices; i++)
            free(gr->arestas[i]);
        free(gr->arestas);

        if(gr->eh_ponderado){
            for(i=0; i<gr->nro_vertices; i++)
                free(gr->pesos[i]);
            free(gr->pesos);
        }
        free(gr->grau);
        free(gr);
    }
}



void pilha_libera (Pilha* p)
{
    Elem *t, *q = p->prim;

    while(q!=NULL)
    {
        t = q->prox;
        free(q);
        q = t;
    }

    free(p);
}



void libera_lista(Elem* li){
    if(li != NULL){
        Elem* no;
        while(li != NULL){
            no = li;
            li = li->prox;
            free(no);
        }
        free(li);
    }
}



 
























































void buscaProfundidade(Grafo *gr, int ini, int *visitado, int cont, Pilha* p){

    // ini == 1 e cont == 1

    visitado[ini] = cont;    // marca o primeiro vetor como uma visita

    // grau == NV grau[] iniciado com 0
                           // 1
    for(int i=0; i < gr->grau[ini]; i++){
        
        if(!visitado[gr->arestas[ini][i]]){
            buscaProfundidade(gr,gr->arestas[ini][i],visitado,cont+1,p);
        }
            

    }

}



Pilha* buscaProfundidade_Grafo(Grafo *gr, int ini, int *visitado){
    int cont = 1;

    // inicializar vetor visitados com 0
    for(int i=0; i<gr->nro_vertices; i++){
        visitado[i] = 0;
    }


    Pilha* p = pilha_cria();

    buscaProfundidade(gr, ini, visitado, cont, p);



    for(int i=0; i < gr->nro_vertices; i++){
        printf("vertice %d -> %d\n",i,visitado[i]);
    }

    return p;


}