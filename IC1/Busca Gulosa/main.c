#include <stdio.h>
#include <stdlib.h>
#include "Lista.h"

int main(){


    //Elemento* lst = lst_cria();
    Coluna* Col = coluna_cria();

    int custos[8]={0,24,15,22,12,7,7,0};
    int visitados[20];
    for (int i = 1; i <= 20; ++i)
        visitados[i] = 0;



    Col = insereColuna(Col, 1);
    Coluna* Aux = Col;
    Col->No = lst_insere(Col->No, 2);
    Col->No = lst_insere(Col->No, 3);
    Col->No = lst_insere(Col->No, 4);

    Col = insereColuna(Col, 2);
    Col->No = lst_insere(Col->No, 1);
    Col->No = lst_insere(Col->No, 4);
    Col->No = lst_insere(Col->No, 5);


    Col = insereColuna(Col, 3);
    Col->No = lst_insere(Col->No, 1);
    Col->No = lst_insere(Col->No, 6);

    Col = insereColuna(Col, 4);
    Col->No = lst_insere(Col->No, 1);
    Col->No = lst_insere(Col->No, 4);
    Col->No = lst_insere(Col->No, 5);
    Col->No = lst_insere(Col->No, 7);

    Col = insereColuna(Col, 5);
    Col->No = lst_insere(Col->No, 2);
    Col->No = lst_insere(Col->No, 4);
    Col->No = lst_insere(Col->No, 7);

    Col = insereColuna(Col, 6);
    Col->No = lst_insere(Col->No, 3);
    Col->No = lst_insere(Col->No, 7);

    Col = insereColuna(Col, 7);
    Col->No = lst_insere(Col->No, 4);
    Col->No = lst_insere(Col->No, 5);
    Col->No = lst_insere(Col->No, 6);



    matrix_imprime(Aux);
    printf("\n\nBusca Gulosa\n\n");

    buscaGulosa(Aux, custos, visitados);

    printf("\n");

    return 0;
}















/*
















































    custos = lst_insere(custos, 24);
    custos = lst_insere(custos, 15);
    custos = lst_insere(custos, 22);
    custos = lst_insere(custos, 12);
    custos = lst_insere(custos, 7);
    custos = lst_insere(custos, 7);
    custos = lst_insere(custos, 0);

*/









    /*

    lst_imprime (lst);

    elem = busca(lst, 10);

    lst_imprime (elem);

    printf("\nRemoção no início \n");
    lst = lst_retira (lst, 33);
    lst_imprime (lst);

    printf("\nRemoção no meio \n");
    lst = lst_retira (lst, 45);
    lst_imprime (lst);

    printf("\nRemoção no fim \n");
    lst = lst_retira (lst, 23);
    lst_imprime (lst);

    printf("\nFaz lista vazia e testa\n");
    lst = lst_retira (lst, 58);
    lst = lst_retira (lst, 10);
    if ( lst_vazia(lst))
        printf("Lista vazia\n");
    lst_imprime (lst);

    printf("\nInserção ordenada\n");
    lst = lst_insere_ordenado(lst, 25);
    lst = lst_insere_ordenado(lst, 12);
    lst = lst_insere_ordenado(lst, 49);
    lst = lst_insere_ordenado(lst, 02);
    lst_imprime (lst);
*/
