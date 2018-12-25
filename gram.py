""" Каждый символ представляется в виде строки;
    vt и vn - множества (set) терминальных и нетерминальных симоволов
    соответственно;
    s - аксиома, множество (set) с едиственным символом;
    p - список (list), каждый член которого - правило;
    правило - список, состоит из правой и левой частей;
    каждая часть - список, состоит из символов."""


def is_empty_word(word):
    """Проверяет, является ли цепочка пустой"""
    for symbol in word:
        if symbol != "_":
            return False
    return True


def bn_to_normal(p):
    """Приводит форму Бэкуса-Наура к обычному виду"""
    p_new = []
    for i in range(len(p)):
        for j in range(len(p[i][1])):
            p_new.append([p[i][0], p[i][1][j]])
    return p_new


def read_file():
    """Считывание файла, парсинг, проверка корректности данных"""
    try:
        with open("in.txt", 'tr', encoding='utf-8') as file_handler:
            l = file_handler.readlines()
    except IOError:
        print("Ошибка чтения файла")
        return None, None, None, None
    finally:
        file_handler.close()
    if len(l) < 4:
        print("Ошибка: в файле недостаточно файлов")
        return None, None, None, None
    for i in range(len(l)):
        l[i] = l[i].strip()
    # print(l)
    l[0] = set(l[0].split())
    l[1] = set(l[1].split())
    l[2] = set(l[2].split())
    # print(l)
    if len(l[0]) == 0 or len(l[1]) == 0 or len(l[2]) == 0:
        print("Данные не определены!")
        return None, None, None, None
    if not l[0].isdisjoint(l[1]):
        print("Множества терминалов и нетерминалов пересекаются!")
        return None, None, None, None
    if len(l[2]) != 1:
        print("Целовой символ может быть только один!")
        return None, None, None, None
    if not l[2] <= l[1]:
        print("Целевой символ должен быть нетерминалом!")
        return None, None, None, None
    v = l[0] | l[1] | {"_"}
    for i in range(3, len(l)):
        l[i] = [s.strip() for s in l[i].split("=>")]
        if len(l[i]) != 2:
            print("Неверно указано правило!")
            return None, None, None, None
        l[i][0] = l[i][0].split()
        if not set(l[i][0]) <= v:
            print("Неверна указана левая часть правила!")
            return None, None, None, None
        l[i][1] = l[i][1].split("|")
        for j in range(len(l[i][1])):
            l[i][1][j] = l[i][1][j].split()
            if not set(l[i][1][j]) <= v:
                print("Неверна указана правая часть правила!")
                return None, None, None, None
    p = [l[i] for i in range(3, len(l))]
    p = bn_to_normal(p)
    return l[0], l[1], l[2], p


def is_type_0(vt, vn, s, p):
    """Тип 0, с фазовой грамматикой: т.к. это самый общий тип, единственное,
    что делает функция:проверяет, чтобы в левой части не было пустой цепочки"""
    for rule in p:
        if is_empty_word(rule[0]):
            return False
    return True

def is_type_1_kz(vt, vn, s, p):
    """Тип 1, контекстно-зависимая грамматика"""
    for rule in p:
        is_right = False
        for i in range(len(rule[0])):
            if rule[0][i] in vn:
                a = rule[0][:i]
                b = rule[0][i+1:]
                if rule[1][:i] == a and rule[1][len(rule[1])-len(b):] == b \
                        and not is_empty_word(rule[1][i:len(rule[1])-len(b)]):
                    is_right = True
                    break
        if not is_right:
            return False
    return True

def is_type_1_nu(vt, vn, s, p):
    """Тип 1,неукорачивающая грамматика"""
    for rule in p:
        if is_empty_word(rule[0]) or is_empty_word(rule[1]) or \
           len(rule[0]) > len(rule[1]):
            return False
    return True


def is_type_2_nks(vt, vn, s, p):
    """Тип 2, неукорачивающая контекстно-свободная грамматика"""
    for rule in p:
        if len(rule[0]) != 1 or not rule[0][0] in vn or is_empty_word(rule[1]):
            return False
    return True


def is_type_2_uks(vt, vn, s, p):
    """Тип 2, укорачивающая контекстно-свободная грамматика"""
    for rule in p:
        if len(rule[0]) != 1 or not rule[0][0] in vn:
            return False
    return True


def is_type_3_left(vt, vn, s, p):
    """Тип 3, регулярная леволинейная грамматика"""
    for rule in p:
        if len(rule[0]) != 1 or not rule[0][0] in vn:
            return False
        if is_empty_word(rule[1]):
            continue
        if len(rule[1]) == 1 and not rule[1][0] in vt:
            return False
        if not (len(rule[1]) == 2 and rule[1][0] in vn and rule[1][1] in vt):
            return False
    return True


def is_type_3_right(vt, vn, s, p):
    """Тип 3, регулярная праволинейная грамматика"""
    for rule in p:
        if len(rule[0]) != 1 or not rule[0][0] in vn:
            return False
        if is_empty_word(rule[1]):
            continue
        if len(rule[1]) == 1 and not rule[1][0] in vt:
            return False
        if not (len(rule[1]) == 2 and rule[1][0] in vt and rule[1][1] in vn):
            return False
    return True


if __name__ == "__main__":
    vt, vn, s, p = read_file()
    g = vt, vn, s, p
    print("G(Vt, Vn, S, P)")
    print("Vt = ", vt)
    print("Vn = ", vn)
    print("S = ", s)
    print('P: ')
    for rule in p:
        print(rule[0], " => ", rule[1])
    print("Тип грамматики")
    print("Тип 0(с фразовой структурой):", "+" if is_type_0(*g) else "-")
    print("Тип 1(контекстно-зависимая):", "+" if is_type_1_kz(*g) else "-")
    print("Тип 1(неукорачиваюшая):", "+" if is_type_1_nu(*g) else "-")
    print("Тип 2(неукорачивающая контекстно-свободная):",
          "+" if is_type_2_nks(*g) else "-")
    print("Тип 2(укорачивающая контекстно-свободная):",
          "+" if is_type_2_uks(*g) else "-")
    print("Тип 3(регулярная леволинейная):",
          "+" if is_type_3_left(*g) else "-")
    print("Тип 3(регулярная праволинейная):",
          "+" if is_type_3_right(*g) else "-")
