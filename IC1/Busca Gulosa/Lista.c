#include <stdio.h>
#include <stdlib.h>
#include "Lista.h"

Elemento* lst_cria(void)
{
    return NULL;
}

Coluna* coluna_cria(void)
{
    return NULL;
}


Coluna* insereColuna(Coluna* col, int valor){

    Coluna* Aux=NULL;

        if(col == NULL){

            Coluna* novo =(Coluna*)malloc(sizeof(Coluna));
            novo->No = NULL;          // tipo Elemento
            novo->proxColuna = NULL;
            novo->info = valor;
            return novo;

        }else{

            Aux = col;

            while(Aux->proxColuna != NULL){
                Aux = Aux->proxColuna;
            }

            Coluna* novo =(Coluna*)malloc(sizeof(Coluna));
            novo->No = NULL;             // tipo Elemento
            novo->proxColuna = NULL;
            novo->info = valor;
            Aux->proxColuna = novo;
        }

        return Aux->proxColuna;


}




Elemento* insereValor(int val){

    Elemento* novo =(Elemento*)malloc(sizeof(Elemento));
    novo->info = val;
    novo->prox = NULL;
    return novo;

}


Elemento* lst_insere(Elemento* lst, int val)
{
    Elemento* Aux=NULL;

    if(lst == NULL){

        lst = insereValor(val);
        return lst;

    }else{

        Aux = lst;

        while(Aux->prox != NULL){
            Aux = Aux->prox;
        }

        Aux->prox = insereValor(val);

    }

    return lst;

}


void lst_imprime (Elemento* lst)
{
    Elemento* p;
    for (p = lst; p != NULL; p = p->prox)
        printf("%d -> ", p->info);
    printf("NULL\n");
}



void matrix_imprime(Coluna* col){

    Coluna* c = col;
    Elemento* Aux = c->No;


    for (c = col; c != NULL; c = c->proxColuna){
        printf("%i - ", c->info);
        for (Aux = c->No; Aux != NULL; Aux = Aux->prox){
            printf("%d -> ", Aux->info);
        }

        printf("NULL\n");

    }


}



Elemento* busca(Elemento* lst, int v)
{
    Elemento* p;
    for (p = lst; p!=NULL; p = p->prox)
    {
        if (p->info == v)
            return p;
    }
    return NULL;
}


Coluna* buscaCol(Coluna* col, int v)
{
    Coluna* c;
    for (c = col; c!=NULL; c = c->proxColuna)
    {
        if (c->info == v)
            return c;
    }
    return NULL;
}



void lst_libera (Elemento* lst)
{
    Elemento *p = lst, *t;
    while (p != NULL)
    {
        t = p->prox;
        free(p);
        p = t;
    }
}



void buscaGulosa(Coluna* col, int* Custos, int* visitados){

    int posicaoMenorRota=0;  // Armazena a menor rota para o próximo vertice
    int menorRota;         // armazena a menor rota para fazer comparações
    int i = col->info;

    Coluna* AuxCol = col;

    Elemento* Aux;

    while(Custos[i] != 0){
        visitados[col->info] = 1;
        Aux = col->No;
        menorRota = Custos[Aux->info];
        printf("\n%i \n", col->info);
        while(Aux != NULL){

            if (visitados[Aux->info] == 0)
            {
                printf("%i - ", Aux->info);
            }
            

            if (menorRota > Custos[Aux->info] && visitados[Aux->info] == 0){
                
                menorRota = Custos[Aux->info];
                posicaoMenorRota = Aux->info;

            }

            Aux = Aux->prox;
        }

        //printf("%i \n", posicaoMenorRota);

        col = buscaCol(AuxCol, posicaoMenorRota);
        i = posicaoMenorRota;

    }

}
































/*


void buscaGulosa(Coluna* col, int* Custos, int* visitados){

    int posicaoMenorRota;  // Armazena a menor rota para o próximo vertice
    int menorRota;         // armazena a menor rota para fazer comparações
    int i = 1;

    Elemento* Aux;

        // usar do, erro no final
        while(Custos[col->info] != 0){
           // Aux = vet[i];
            printf("%i ", col->info);     // posteriormente usa vetor de char
            visitados[col->info]=1;
            menorRota = Custos[Aux->info+1];   // +1 para contornar o erro de 0

            while(Aux != NULL){
                if(menorRota > Custos[Aux->info+1] && visitados[i] == 0){
                    menorRota = Custos[Aux->info+1];
                    posicaoMenorRota = Aux->info;
                }
                printf("%i ", Aux->info); // vai imprimindo os nos do vertice
                Aux = Aux->prox;
            }

            i=posicaoMenorRota;
            printf("\n");
        }


}


*/