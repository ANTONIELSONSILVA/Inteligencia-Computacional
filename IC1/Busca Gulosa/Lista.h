//Lista encadeada de inteiros sem n� cabe�a

struct elemento
{
    int info;
    struct elemento *prox;
};
typedef struct elemento Elemento;


struct coluna
{
    int info;
    Elemento* No;
    struct coluna *proxColuna;
};
typedef struct coluna Coluna;



//fun��o de cria��o: retorna uma lista vazia
Elemento* lst_cria (void);

//inser��o no in�cio: retorna a lista atualizada
Elemento* lst_insere (Elemento* lst, int val);

//imprime os valores dos elementos armazenados
void lst_imprime (Elemento* lst);

//fun��o vazia: retorna 1 se vazia ou 0 se n�o vazia
int lst_vazia (Elemento* lst);

//recebe a informa��o referente ao elemento a pesquisar
//retorna o ponteiro do n� da lista que representa o elemento, ou NULL, caso o elemento n�o seja encontrado na lista
Elemento* busca (Elemento* lst, int v);


//destr�i a lista, liberando todos os elementos alocados
void lst_libera (Elemento* lst);


Coluna* coluna_cria(void);

Coluna* insereColuna(Coluna* col, int valor);

void matrix_imprime (Coluna* col);

void buscaGulosa(Coluna* col, int* Custos, int* visitados);
