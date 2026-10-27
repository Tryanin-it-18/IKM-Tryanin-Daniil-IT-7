"""Собственные динамические структуры данных для двух заданий."""


class StackNode:
    """Узел односвязного стека: значение и ссылка на следующий узел."""

    def __init__(self, value, next_node=None):
        self.value = value
        self.next = next_node


class Stack:
    """Стек на односвязном списке (LIFO)."""

    def __init__(self):
        self.top = None
        self.length = 0

    def push(self, value):
        self.top = StackNode(value, self.top)
        self.length += 1

    def pop(self):
        if self.top is None:
            raise ValueError("Нельзя извлечь элемент из пустого стека.")
        value = self.top.value
        self.top = self.top.next
        self.length -= 1
        return value

    def peek(self):
        if self.top is None:
            raise ValueError("Стек пуст.")
        return self.top.value

    def is_empty(self):
        return self.top is None

    def __len__(self):
        return self.length


class ChildLink:
    """Звено односвязного списка дочерних вершин дерева."""

    def __init__(self, child, next_link=None):
        self.child = child
        self.next = next_link


class TreeNode:
    """Вершина дерева: номер гнезда, количество писем и ссылки на детей."""

    def __init__(self, number, letters):
        self.number = number
        self.letters = letters
        self.parent = None
        self.children = None
        self.depth = 0
        self.needed = letters > 0

    def add_child(self, child):
        self.children = ChildLink(child, self.children)
        child.parent = self

    def iter_children(self):
        link = self.children
        while link is not None:
            yield link.child
            link = link.next


class Tree:
    """Дерево с корнем в гнезде № 1."""

    def __init__(self, nodes):
        self.nodes = nodes
        self.root = nodes[1]
