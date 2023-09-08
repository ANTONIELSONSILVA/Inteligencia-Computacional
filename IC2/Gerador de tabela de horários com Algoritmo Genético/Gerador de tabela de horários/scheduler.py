import random
from operator import itemgetter
from utils import carregarDados, show_timetable, preenche, mostraEstatisticas, write_solution_to_file
from costs import checar_aptidoes, Calcula_aptidoes, empty_space_groups_cost, empty_space_teachers_cost, \
    horas_livres
import copy
import math

#   A proposta do algoritmo é achar uma solução genérica para realizar a montagem
#   de uma grade de horários para as disciplinas de um semestre de uma faculdade

#   Variáveis de entrada: Nome do professor, disciplina, tipo de aula(teórica, exercícios, laboratorial), duração
#   e a lista de salas permitidas

#   Variáveis de saída: A sala e o tempo para cada aula

#   Restrições:
#       Rígidas:
#           . Nenhum professor pode dar duas aulas ao mesmo tempo
#           . Nenhuma turma pode assistir a duas aulas ao mesmo tempo
#           . Nenhuma sala pode ter duas aulas ao mesmo tempo
#           . A aula deve ser ministrada em uma das salas permitidas
#       Leves:
#           . Se a disciplina possuir vários métodos de ensinamento, a ordem preferida deve ser: aula teórica, exercícios, aula laboratorial

#   Objetivos:
#       . Respeitar as restrições rígidas
#       . Respeitar as restrições leves
#       . Minimizar o tempo ocioso de cada grupo
#       . Minimizar o tempo ocioso de cada professor
#       . Provisionar uma hora em uma semana de aulas em que ninguém tenha aula



# inicia a população

def população_inicial(data, matrix, livre, preenchidas, groups_empty_space, teachers_empty_space, subjects_order):
    """
     Configura o horário inicial para determinadas aulas inserindo em campos livres de forma que cada aula esteja em seu ajuste
     Sala de aula.
     """
    disciplinas = data.disciplinas

    for index, classs in disciplinas.items():
        ind = 0
        while True:
            campo_inicial = livre[ind]

            # verifica se a aula não vai começar em um dia e terminar no outro
            horaDEinício = campo_inicial[0]
            end_time = horaDEinício + int(classs.duration) - 1
            if horaDEinício % 12 > end_time % 12:
                ind += 1
                continue

            found = True
            # verifica se o bloco inteiro da aula está livre
            for i in range(1, int(classs.duration)):
                field = (i + horaDEinício, campo_inicial[1])
                if field not in livre:
                    found = False
                    ind += 1
                    break

            # garantir que a sala de aula se encaixe
            if campo_inicial[1] not in classs.classrooms:
                ind += 1
                continue

            if found:
                for group_index in classs.groups:
                    # adiciona ordem dos assuntos para o grupo
                    insert_order(subjects_order, classs.subject, group_index, classs.type, horaDEinício)
                    # adiciona os horários da aula para o grupo
                    for i in range(int(classs.duration)):
                        groups_empty_space[group_index].append(i + horaDEinício)

                for i in range(int(classs.duration)):
                    preenchidas.setdefault(index, []).append((i + horaDEinício, campo_inicial[1]))        # add to filled
                    livre.remove((i + horaDEinício, campo_inicial[1]))                                # remove from free
                    # adiciona horários da aula para professores
                    teachers_empty_space[classs.teacher].append(i + horaDEinício)
                break

    #preenche a matriz
    for index, fields_list in preenchidas.items():
        for field in fields_list:
            matrix[field[0]][field[1]] = index


#Insere a hora de início da aula para determinado assunto, grupo e Modeloo de aula.
def insert_order(subjects_order, subject, grupo, Modeloo, hora_de_início):

    times = subjects_order[(subject, grupo)]
    if Modeloo == 'P':
        times[0] = hora_de_início
    elif Modeloo == 'V':
        times[1] = hora_de_início
    else:
        times[2] = hora_de_início
    subjects_order[(subject, grupo)] = times





    #Retorna se a turma puder estar nessa linha devido a possíveis sobreposições de professores ou grupos.

def linhaValidaprofessores(matrix, dados, index_class, linhas):

    c1 = dados.disciplinas[index_class]
    for j in range(len(matrix[linhas])):
        if matrix[linhas][j] is not None:
            c2 = dados.disciplinas[matrix[linhas][j]]
            #verificar professor
            if c1.teacher == c2.teacher:
                return False
            # verificar grupos
            for g in c2.groups:
                if g in c1.groups:
                    return False
    return True


def ponto_ideal_de_mutação(matrix, data, ind_class, free, filled, groups_empty_space, teachers_empty_space, subjects_order):
    """
     Função que tenta encontrar novos campos na matriz para índice de disciplina onde o custo da disciplina é 0 (levado em
     conta apenas restrições rígidas). Se o local ideal for encontrado, os campos na matriz serão substituídos.
     """

    # encontra linhas e campos em que a disciplina está atualmente
    rows = []
    fields = filled[ind_class]
    for f in fields:
        rows.append(f[0])

    classs = data.disciplinas[ind_class]
    ind = 0
    while True:
        # local ideal não foi encontrado, retorna da função
        if ind >= len(free):
            return
        start_field = free[ind]

        # verifica se a aula não vai começar em um dia e terminar no outro
        start_time = start_field[0]
        end_time = start_time + int(classs.duration) - 1
        if start_time % 12 > end_time % 12:
            ind += 1
            continue

        # verifica se a nova sala de aula é adequada
        if start_field[1] not in classs.classrooms:
            ind += 1
            continue

        # verificar se o bloco inteiro pode ser ocupado para nova turma e possíveis sobreposições com professores e grupos
        found = True
        for i in range(int(classs.duration)):
            field = (i + start_time, start_field[1])
            if field not in free or not linhaValidaprofessores(matrix, data, ind_class, field[0]):
                found = False
                ind += 1
                break

        if found:
            # remove uma disciplina atual do dict preenchido e adiciona ao dict livre
            filled.pop(ind_class, None)
            for f in fields:
                free.append((f[0], f[1]))
                matrix[f[0]][f[1]] = None
                # remove o espaço vazio do grupo do antigo local da disciplina
                for group_index in classs.groups:
                    groups_empty_space[group_index].remove(f[0])
                # remove o espaço vazio do professor do antigo local da turma
                teachers_empty_space[classs.teacher].remove(f[0])

            # atualiza a ordem dos assuntos e adiciona espaço vazio para cada grupo
            for group_index in classs.groups:
                insert_order(subjects_order, classs.subject, group_index, classs.type, start_time)
                for i in range(int(classs.duration)):
                    groups_empty_space[group_index].append(i + start_time)

            # adiciona novo termo da disciplina a ser preenchida, remove esses campos do free dict e insere novo bloco na matriz
            for i in range(int(classs.duration)):
                filled.setdefault(ind_class, []).append((i + start_time, start_field[1]))
                free.remove((i + start_time, start_field[1]))
                matrix[i + start_time][start_field[1]] = ind_class
                # adiciona um novo espaço vazio para o professor
                teachers_empty_space[classs.teacher].append(i+start_time)
            break


def algoritmo_genético(matrix, data, free, filled, groups_empty_space, teachers_empty_space, subjects_order):

    #Algoritmo evolutivo que se cansa de encontrar uma programação tal que as restrições rígidas sejam satisfeitas.
    #Ele usa (1+1) estratégia evolutiva com notação de Stifel.

    # variáveis de inicialização
    n = 3
    sigma = 2
    run_times = 5
    max_stagnation = 200

    for run in range(run_times):
        print('Run {} | sigma = {}'.format(run + 1, sigma))

        t = 0
        stagnation = 0
        cost_stats = 0

        while stagnation < max_stagnation:

            # verifica se a solução ótima foi encontrada

            # APTIDÃO, checar se as restrições foram satisfeitas  
            loss_before, cost_disciplinas, cost_teachers, cost_classrooms, cost_groups = Calcula_aptidoes(matrix, data)
            if loss_before == 0 and checar_aptidoes(matrix, data) == 0:
                print('Solução ideal encontrada: \n')
                show_timetable(matrix)
                break
            #-------------------------------------------------

            # caso a etapa anterior não detecta uma solução, fazemos a seleção de indivíduos para cruzamento
            # classifica as disciplinas por sua perda, [(perda, índice de disciplina)]
            costs_list = sorted(cost_disciplinas.items(), key=itemgetter(1), reverse=True)



            # Verificação da necessidade ou não de mutação
            for i in range(len(costs_list) // 4):
                #gera a mutação
                # mutar um para o local ideal
                if random.uniform(0, 1) < sigma and costs_list[i][1] != 0:
                    ponto_ideal_de_mutação(matrix, data, costs_list[i][0], free, filled, groups_empty_space,
                                      teachers_empty_space, subjects_order)


            # calculo da aptidões que no caso são as restições
            loss_after, _, _, _, _ = Calcula_aptidoes(matrix, data)

            #Operadores de cruzamento com probabilidade pc
            if loss_after < loss_before:
                stagnation = 0
                cost_stats += 1
            else:
                stagnation += 1

            t += 1
            if t >= 10*n and t % n == 0:
                s = cost_stats
                if s < 2*n:
                    sigma *= 0.85
                else:
                    sigma /= 0.85
                cost_stats = 0

        # imprime o resultado do cruzamento e retorma para o próximo ciclo para procurar a próxima solução


        print('Número de iterações: {} \nCusto: {} \nCusto dos professores: {} | Custo do grupo: {} | Custo da aula:'
              ' {}'.format(t, loss_after, cost_teachers, cost_groups, cost_classrooms))




def main():

    #free = [(linha, coluna)...] - lista de campos livres (linha, coluna) na matriz
    #preenchido: dicionário onde chave = índice da disciplina, valor = lista de campos na matriz

    #assuntos_ordem: dicionário onde chave = (nome do assunto, índice do grupo), valor = [int, int, int]
    #onde ints representam os horários de início (linha na matriz) para Modeloos de disciplinas P, V e L respectivamente
    #groups_empty_space: dicionário onde chave = índice do grupo, valores = lista de linhas onde está
    #professores_empty_space: dicionário onde chave = nome do professor, valores = lista de linhas onde está

    #matriz = colunas são salas de aula, linhas são tempos, cada campo tem índice da turma ou está vazio
    #dados = dados de entrada, contém turmas, salas de aula, professores e grupos

    filled = {}
    subjects_order = {}
    groups_empty_space = {}
    teachers_empty_space = {}
    file = 'Quadro_Horarios.txt'

    dados = carregarDados('test_files/' + file, teachers_empty_space, groups_empty_space, subjects_order)
    matrix, free = preenche(len(dados.classrooms))
    população_inicial(dados, matrix, free, filled, groups_empty_space, teachers_empty_space, subjects_order)

    #Avalia a população com base no cálculo do custo total de restrições
    total, _, _, _, _ = Calcula_aptidoes(matrix, dados)
    print('Custo inicial de restrições rígidas: {}'.format(total))

    algoritmo_genético(matrix, dados, free, filled, groups_empty_space, teachers_empty_space, subjects_order)

    print('ESTATISTICAS')
    mostraEstatisticas(matrix, dados, subjects_order, groups_empty_space, teachers_empty_space)


if __name__ == '__main__':
    main()
