import json
import random
from costs import checar_aptidoes, subjects_order_cost, empty_space_groups_cost, empty_space_teachers_cost, \
    horas_livres
from model import Class, Classroom, Data


def carregarDados(file_path, teachers_empty_space, groups_empty_space, subjects_order):
    """
    Carrega e processa os dados de input, inicializa as estruturas auxiliares.
    :param file_path: path para o arquivo com os dados de input.
    :param teachers_empty_space: dicionário aonde chave = nome do professor, values = lista de linhas aonde ele está inserido.
    :param groups_empty_space: dicionário aonde chave = índice do grupo, values = lista de linhas aonde ele está inserido.
    :param subjects_order: dicinário aonde chave = (nome da disciplina, índice do grupo), value = [int, int, int]
    aonde int's representam os tempos de início (linha da matriz) para tipos de disciplinas P, V e L respectivamente. Se o tempo de início for -1
    significa que essa disciplina não possui esse tipo de classe.
    :return: Data(groups, teachers, disciplinas, classrooms)
    """
    with open(file_path) as file:
        data = json.load(file)

    # disciplinas: dictionary where key = index of a class, value = class
    disciplinas = {}
    # classrooms: dictionary where key = index, value = classroom name
    classrooms = {}
    # teachers: dictionary where key = teachers' name, value = index
    teachers = {}
    # groups: dictionary where key = name of the group, value = index
    groups = {}
    class_list = []

    for cl in data['Casovi']:
        new_group = cl['Turma']
        new_teacher = cl['Professor(a)']

        #inicializa espaço vazio de professores
        if new_teacher not in teachers_empty_space:
            teachers_empty_space[new_teacher] = []

        new = Class(new_group, new_teacher, cl['disciplina'], cl['Modelo'], cl['Trajanje'], cl['A sala de aula'])
        # adiciona os grupos
        for group in new_group:
            if group not in groups:
                groups[group] = len(groups)
                # inicializa espaço vazio de grupos
                groups_empty_space[groups[group]] = []

        # adiciona professor
        if new_teacher not in teachers:
            teachers[new_teacher] = len(teachers)
        class_list.append(new)


    # embaralha mais por causa dos professores
    random.shuffle(class_list)
    # adiciona salas
    for cl in class_list:
        disciplinas[len(disciplinas)] = cl

    # cada classe é associada a lista de salas que ela pode estar como índice (colunas mais distantes da matriz)
    for type in data['Ucionice']:
        for name in data['Ucionice'][type]:
            new = Classroom(name, type)
            classrooms[len(classrooms)] = new

    # cada classe tem uma lista de grupos marcados pelo índice, o mesmo para as salas
    for i in disciplinas:
        cl = disciplinas[i]

        classroom = cl.classrooms
        index_classrooms = []
        # adiciona salas
        for index, c in classrooms.items():
            if c.type == classroom:
                index_classrooms.append(index)
        cl.classrooms = index_classrooms

        class_groups = cl.groups
        index_groups = []
        for name, index in groups.items():
            if name in class_groups:
                # inicializa a ordem das disciplinas
                if (cl.subject, index) not in subjects_order:
                    subjects_order[(cl.subject, index)] = [-1, -1, -1]
                index_groups.append(index)
        cl.groups = index_groups

    return Data(groups, teachers, disciplinas, classrooms)


def preenche(num_of_columns):
    """
    Preenche a tabela de horários e o dicionário que armazenam campos livres da matriz.
    :param num_of_columns: números de salas
    :return: matriz, livre
    """
    w, h = num_of_columns, 60                                          # 5 (dias úteis) * 12 (horas de trabalho) = 60
    matrix = [[None for x in range(w)] for y in range(h)]
    free = []

    # initialise free dict as all the fields from matrix
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            free.append((i, j))
    return matrix, free


def show_timetable(matrix):
    """
    Imprime a tabela de horários
    """
    days = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta']
    hours = [9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]

    # print heading for classrooms
    for i in range(len(matrix[0])):
        if i == 0:
            print('{:17s} C{:6s}'.format('', '0'), end='')
        else:
            print('C{:6s}'.format(str(i)), end='')
    print()

    d_cnt = 0
    h_cnt = 0
    for i in range(len(matrix)):
        day = days[d_cnt]
        hour = hours[h_cnt]
        print('{:10s} {:2d} ->  '.format(day, hour), end='')
        for j in range(len(matrix[i])):
            print('{:6s} '.format(str(matrix[i][j])), end='')
        print()
        h_cnt += 1
        if h_cnt == 12:
            h_cnt = 0
            d_cnt += 1
            print()


def write_solution_to_file(matrix, data, filled, filepath, groups_empty_space, teachers_empty_space, subjects_order):
    """
    Escreve estatísticas e horários no arquivo
    """
    f = open('solution_files/sol_' + filepath, 'w')

    f.write('-------------------------- STATISTICS --------------------------\n')
    cost_hard = checar_aptidoes(matrix, data)
    if cost_hard == 0:
        f.write('\nRestrições rígidas satisfeitas: 100.00 %\n')
    else:
        f.write('Restrições rígidas NÃO satisfeitas, custo: {}\n'.format(cost_hard))
    f.write('Restrições suaves satisfeitas: {:.02f} %\n\n'.format(subjects_order_cost(subjects_order)))

    empty_groups, max_empty_group, average_empty_groups = empty_space_groups_cost(groups_empty_space)
    f.write('Espaço vazio total para todos os grupos e todos os dias: {}\n'.format(empty_groups))
    f.write('Espaço vazio máximo para o GRUPO em um dia: {}\n'.format(max_empty_group))
    f.write('Espaço vazio médio para GRUPOS por semana: {:.02f}\n\n'.format(average_empty_groups))

    empty_teachers, max_empty_teacher, average_empty_teachers = empty_space_teachers_cost(teachers_empty_space)
    f.write('Espaço vazio total para todos os PROFESSORES e todos os dias: {}\n'.format(empty_teachers))
    f.write('Espaço vazio máximo para PROFESSORES em um dia: {}\n'.format(max_empty_teacher))
    f.write('Espaço vazio médio para PROFESSORES por semana: {:.02f}\n\n'.format(average_empty_teachers))

    f_hour = horas_livres(matrix)
    if f_hour != -1:
        f.write('Horário livre -> {}\n'.format(f_hour))
    else:
        f.write('Nenhum horário sem disciplinas.\n')

    groups_dict = {}
    for group_name, group_index in data.groups.items():
        if group_index not in groups_dict:
            groups_dict[group_index] = group_name
    days = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta']
    hours = [9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]

    f.write('\n--------------------------- SCHEDULE ---------------------------')
    for class_index, times in filled.items():
        c = data.disciplinas[class_index]
        groups = ' '
        for g in c.groups:
            groups += groups_dict[g] + ', '
        f.write('\n\nClasse {}\n'.format(class_index))
        f.write('Professor: {} \nDisciplina: {} \nGrupo:{} \nTipo: {} \nDuração: {} hora(s)'
                .format(c.teacher, c.subject, groups[:len(groups) - 2], c.type, c.duration))
        room = str(data.classrooms[times[0][1]])
        f.write('\nSala: {:2s}\nTempo: {}'.format(room[:room.rfind('-')], days[times[0][0] // 12]))
        for time in times:
            f.write(' {}'.format(hours[time[0] % 12]))
    f.close()


def mostraEstatisticas(matrix, data, subjects_order, groups_empty_space, teachers_empty_space):
    """
    Imprime Estatísticas.
    """
    cost_hard = checar_aptidoes(matrix, data)
    if cost_hard == 0:
        print('Restrições rígidas satisfeitas: 100,00%')
    else:
        print('Restrições rígidas NÃO satisfeitas, custo: {}'.format(cost_hard))
    print('Restrições suaves satisfeitas: {:.02f} %\n'.format(subjects_order_cost(subjects_order)))

    empty_groups, max_empty_group, average_empty_groups = empty_space_groups_cost(groups_empty_space)
    print('TOTAL de espaço vazio para todos os GRUPOS e todos os dias: ', empty_groups)
    print('máximo espaço vazio para o grupo no dia: ', max_empty_group)
    print('MÉDIA de espaço vazio para GRUPOS por semana: {:.02f}\n'.format(average_empty_groups))

    empty_teachers, max_empty_teacher, average_empty_teachers = empty_space_teachers_cost(teachers_empty_space)
    print('TOTAL de espaço vazio para todos os PROFESSORES e todos os dias: ', empty_teachers)
    print('Máximo espaço vazio para PROFESSOR em dia: ', max_empty_teacher)
    print('MÉDIA de espaço vazio para PROFESSORES por semana: {:.02f}\n'.format(average_empty_teachers))

    f_hour = horas_livres(matrix)
    if f_hour != -1:
        print('Tempo livre ->', f_hour)
    else:
        print('SEM horas sem disciplinas.')
