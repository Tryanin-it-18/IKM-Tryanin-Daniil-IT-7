"""Задание № 17 «Почтальон»: поиск минимального числа извинений."""

from structures import Stack, Tree, TreeNode


def read_tree(filename):
    """Прочитать из файла корректное неориентированное дерево с письмами."""
    try:
        with open(filename, "r", encoding="utf-8-sig") as data_file:
            lines = [line.strip() for line in data_file]
    except OSError as error:
        raise ValueError(f"Не удалось открыть файл: {error}") from error

    if not lines or not lines[0]:
        raise ValueError("Файл пуст или в нём отсутствует число гнёзд.")

    try:
        header = [int(value) for value in lines[0].split()]
    except ValueError as error:
        raise ValueError("Первая строка должна содержать одно целое число M.") from error
    if len(header) != 1:
        raise ValueError("В первой строке должно быть только число M.")
    count = header[0]
    if not 1 <= count <= 999:
        raise ValueError("Количество гнёзд M должно быть от 1 до 999.")

    if len(lines) != count + 1:
        raise ValueError(
            f"После M должно быть ровно {count} строк с описанием гнёзд."
        )

    nodes = [None] * (count + 1)
    adjacency = [None] * (count + 1)

    for number in range(1, count + 1):
        try:
            parts = [int(value) for value in lines[number].split()]
        except ValueError as error:
            raise ValueError(f"Строка гнезда {number} содержит нецелые числа.") from error
        if len(parts) < 2:
            raise ValueError(f"Недостаточно данных у гнезда {number}.")
        degree, letters = parts[0], parts[1]
        if degree < 0 or letters < 0:
            raise ValueError(
                "Число соседей и количество писем не могут быть отрицательными."
            )
        neighbors = parts[2:]
        if degree != len(neighbors):
            raise ValueError(f"У гнезда {number} число соседей не совпадает с n_i.")
        if any(
            neighbor < 1 or neighbor > count or neighbor == number
            for neighbor in neighbors
        ):
            raise ValueError(f"Некорректный номер соседа у гнезда {number}.")
        if len(neighbors) != len(set(neighbors)):
            raise ValueError(
                f"У гнезда {number} один сосед указан несколько раз."
            )
        nodes[number] = TreeNode(number, letters)
        adjacency[number] = neighbors

    if sum(len(neighbors) for neighbors in adjacency[1:]) != 2 * (count - 1):
        raise ValueError("Количество связей не соответствует дереву.")

    for number in range(1, count + 1):
        for neighbor in adjacency[number]:
            if number not in adjacency[neighbor]:
                raise ValueError("Связи между гнёздами должны быть двусторонними.")

    tree = Tree(nodes)
    stack = Stack()
    stack.push(nodes[1])
    visited = {1}
    order = []

    while not stack.is_empty():
        node = stack.pop()
        order.append(node)
        for neighbor_number in adjacency[node.number]:
            if node.parent is not None and neighbor_number == node.parent.number:
                continue
            if neighbor_number in visited:
                raise ValueError(
                "Обнаружен цикл: входные данные не образуют дерево."
            )
            visited.add(neighbor_number)
            child = nodes[neighbor_number]
            child.depth = node.depth + 1
            node.add_child(child)
            stack.push(child)

    if len(visited) != count:
        raise ValueError("Дерево не связно: часть гнёзд недоступна.")

    return tree, order


def minimum_apologies(tree, order):
    """Найти оптимальный маршрут по минимальному необходимому поддереву."""
    letters_count = 0
    maximum_depth = 0

    for node in order:
        if node.letters > 0:
            letters_count += 1
            maximum_depth = max(maximum_depth, node.depth)

    if letters_count == 0:
        return 0

    for node in reversed(order):
        if node.needed and node.parent is not None:
            node.parent.needed = True

    required_edges = sum(
        1 for node in order if node.parent is not None and node.needed
    )

    # Каждое ребро нужного поддерева проходится дважды, кроме пути
    # от корня до конечного (самого дальнего) гнезда.
    visits = 2 * required_edges - maximum_depth + 1

    # На первом посещении адресату передают все письма; остальные
    # посещения гнёзд происходят без вручения корреспонденции.
    return visits - letters_count


def solve_postman(filename):
    tree, order = read_tree(filename)
    return minimum_apologies(tree, order)


def save_postman_result(input_filename, output_filename):
    """Вычислить ответ и записать одно число в выходной файл."""
    result = solve_postman(input_filename)
    try:
        with open(output_filename, "w", encoding="utf-8") as output_file:
            output_file.write(f"{result}\n")
    except OSError as error:
        raise ValueError(f"Не удалось записать результат: {error}") from error
    return result
