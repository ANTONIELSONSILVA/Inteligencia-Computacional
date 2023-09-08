//Lista encadeada de inteiros sem nó cabeça

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



//função de criação: retorna uma lista vazia
Elemento* lst_cria (void);

//inserção no início: retorna a lista atualizada
Elemento* lst_insere (Elemento* lst, int val);

//imprime os valores dos elementos armazenados
void lst_imprime (Elemento* lst);

//função vazia: retorna 1 se vazia ou 0 se não vazia
int lst_vazia (Elemento* lst);

//recebe a informação referente ao elemento a pesquisar
//retorna o ponteiro do nó da lista que representa o elemento, ou NULL, caso o elemento não seja encontrado na lista
Elemento* busca (Elemento* lst, int v);


//destrói a lista, liberando todos os elementos alocados
void lst_libera (Elemento* lst);


Coluna* coluna_cria(void);

Coluna* insereColuna(Coluna* col, int valor);

void matrix_imprime (Coluna* col);

void buscaGulosa(Coluna* col, int* Custos, int* visitados);
