def subjects_order_cost(subjects_order):
    """
    Calcula a porcentagem de restrições suaves - ordem das disciplinas (P, V, L).
    :param subjects_order: dicinário aonde chave = (nome da disciplina, índice do grupo), value = [int, int, int]
    aonde int's representam o tempo de início (linha da matriz) para tipos de disciplinas P, V e L respectivamente. Se o tempo de início for -1
    significa que essa disciplina não possui esse tipo de classe.
    :return: porcentagem de restrições satisfeitas.
    """
    # number of subjects not in right order
    cost = 0
    # number of all orders of subjects
    total = 0

    for (subject, group_index), times in subjects_order.items():

        if times[0] != -1 and times[1] != -1:
            total += 1
            # P after V
            if times[0] > times[1]:
                cost += 1

        if times[0] != -1 and times[2] != -1:
            total += 1
            # P after L
            if times[0] > times[2]:
                cost += 1

        if times[1] != -1 and times[2] != -1:
            total += 1
            # V after L
            if times[1] > times[2]:
                cost += 1

    # print(cost, total)
    return 100 * (total - cost) / total


def empty_space_groups_cost(groups_empty_space):

    #Calcula o espaço vazio total de todos os grupos por semana, espaço vazio máximo no dia e espaço vazio médio para todo
    #semana por grupo.
    #:param groups_empty_space: dicionário onde chave = índice do grupo, valores = lista de linhas onde está
    #:return: custo total, máximo por dia, custo médio
    
    # espaço vazio total de todos os grupos durante toda a semana
    cost = 0
    # máximo de espaço vazio em um dia para algum grupo
    max_empty = 0

    for group_index, times in groups_empty_space.items():
        times.sort()
        # espaço vazio para cada dia para o grupo atual
        empty_per_day = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0}

        for i in range(1, len(times) - 1):
            a = times[i-1]
            b = times[i]
            diff = b - a
            # as disciplinas estão no mesmo dia se o horário div 12 for o mesmo
            if a // 12 == b // 12 and diff > 1:
                empty_per_day[a // 12] += diff - 1
                cost += diff - 1

        # compare o máximo atual com espaços vazios por dia para o grupo atual
        for key, value in empty_per_day.items():
            if max_empty < value:
                max_empty = value

    return cost, max_empty, cost / len(groups_empty_space)


def empty_space_teachers_cost(teachers_empty_space):

    #Calcula o espaço vazio total de todos os professores por semana, espaço vazio máximo no dia e espaço vazio médio para todo
    #semana por professor.
    #:param professores_empty_space: dicionário onde chave = nome do professor, valores = lista de linhas onde está
    #:return: custo total, máximo por dia, custo médio

     # total de espaço vazio de todos os professores durante toda a semana

    cost = 0
    # máximo de espaço vazio em um dia para algum professor
    max_empty = 0

    for teacher_name, times in teachers_empty_space.items():
        times.sort()
        # espaço vazio para cada dia para o professor atual
        empty_per_day = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0}

        for i in range(1, len(times) - 1):
            a = times[i - 1]
            b = times[i]
            diff = b - a
            # as disciplinas estão no mesmo dia se o horário div 12 for o mesmo
            if a // 12 == b // 12 and diff > 1:
                empty_per_day[a // 12] += diff - 1
                cost += diff - 1

        # compare o máximo atual com os espaços vazios por dia para o professor atual
        for key, value in empty_per_day.items():
            if max_empty < value:
                max_empty = value

    return cost, max_empty, cost / len(teachers_empty_space)


def horas_livres(matrix):
    """
    Verifica se há uma hora sem disciplinas. Se sim, retorna no formato 'dia: hora', caso contrário -1.
    """
    days = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta']
    hours = [9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]

    for i in range(len(matrix)):
        exists = True
        for j in range(len(matrix[i])):
            field = matrix[i][j]
            if field is not None:
                exists = False

        if exists:
            return '{}: {}'.format(days[i // 12], hours[i % 12])

    return -1


def Calcula_aptidoes(matrix, data):


    #Calcula o custo total de restrições rígidas: em cada sala de aula é no máximo uma aula por vez, cada aula está em uma
    #de suas possíveis salas de aula, cada professor tem no máximo uma aula por vez e cada grupo assiste no máximo uma aula.
    #aula por vez.
    #Para tudo que não satisfaça essas restrições, uma é adicionada ao custo.
    #:retorno: custo total, custo por aula, custo dos professores, custo das salas de aula, custo dos grupos
 
    #cost_class: dicionário onde chave = índice de uma classe, valor = custo total dessa classe

    cost_class = {}
    for c in data.disciplinas:
        cost_class[c] = 0

    cost_classrooms = 0
    cost_teacher = 0
    cost_group = 0
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            field = matrix[i][j]                                        # for every field in matrix
            if field is not None:
                c1 = data.disciplinas[field]                                # take class from that field

                # calculate loss for classroom
                if j not in c1.classrooms:
                    cost_classrooms += 1
                    cost_class[field] += 1

                for k in range(j + 1, len(matrix[i])):                  # go through the end of row
                    next_field = matrix[i][k]
                    if next_field is not None:
                        c2 = data.disciplinas[next_field]                   # take class of that field

                        # calculate loss for teachers
                        if c1.teacher == c2.teacher:
                            cost_teacher += 1
                            cost_class[field] += 1

                        # calculate loss for groups
                        g1 = c1.groups
                        g2 = c2.groups
                        for g in g1:
                            if g in g2:
                                cost_group += 1
                                cost_class[field] += 1

    total_cost = cost_teacher + cost_classrooms + cost_group
    return total_cost, cost_class, cost_teacher, cost_classrooms, cost_group


def checar_aptidoes(matrix, data):
    """
    Verifica se todas as restrições rígidas foram atendidas, retorna o número de sobreposições com disciplinas, salas de aula, professores e
    grupos.
    """
    overlaps = 0
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            field = matrix[i][j]                                    # para cada campo na matriz
            if field is not None:
                c1 = data.disciplinas[field]                            # ter aula desse campo

                # calcular perda para sala de aula
                if j not in c1.classrooms:
                    overlaps += 1

                for k in range(len(matrix[i])):                     # ir até o final da linha
                    if k != j:
                        next_field = matrix[i][k]
                        if next_field is not None:
                            c2 = data.disciplinas[next_field]           # ter aula desse campo

                            # calcular perda para professores
                            if c1.teacher == c2.teacher:
                                overlaps += 1

                            # calcular perda para grupos
                            g1 = c1.groups
                            g2 = c2.groups
                            # print(g1, g2)
                            for g in g1:
                                if g in g2:
                                    overlaps += 1

    return overlaps
