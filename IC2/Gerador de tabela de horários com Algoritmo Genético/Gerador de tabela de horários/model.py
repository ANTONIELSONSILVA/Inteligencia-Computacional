class Class:

    def __init__(self, groups, teacher, subject, type, duration, classrooms):
        self.groups = groups
        self.teacher = teacher
        self.subject = subject
        self.type = type
        self.duration = duration
        self.classrooms = classrooms

    def __str__(self):
        return "Grupos {} | Professor '{}' | Disciplina '{}' | Tipo {} | {} Horário | Salas {} \n"\
            .format(self.groups, self.teacher, self.subject, self.type, self.duration, self.classrooms)

    def __repr__(self):
        return str(self)


class Classroom:

    def __init__(self, name, type):
        self.name = name
        self.type = type

    def __str__(self):
        return "{} - {} \n".format(self.name, self.type)

    def __repr__(self):
        return str(self)


class Data:

    def __init__(self, groups, teachers, disciplinas, classrooms):
        self.groups = groups
        self.teachers = teachers
        self.disciplinas = disciplinas
        self.classrooms = classrooms
