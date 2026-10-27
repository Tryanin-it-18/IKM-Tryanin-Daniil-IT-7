"""Задание № 1: операции m и M с использованием собственного стека."""

from structures import Stack


class Operation:
    """Незавершённая операция с отметкой о встреченной запятой."""

    def __init__(self, name):
        self.name = name
        self.comma_found = False


def calculate_expression(expression):
    """Вычислить выражение m(a,b) / M(a,b) с возможной вложенностью."""
    if not expression:
        raise ValueError("Выражение пустое.")
    if any(symbol.isspace() for symbol in expression):
        raise ValueError("Пробелы внутри выражения не допускаются.")

    values = Stack()
    operations = Stack()
    index = 0
    expect_value = True

    while index < len(expression):
        symbol = expression[index]

        if expect_value:
            if symbol.isascii() and symbol.isdigit():
                end = index
                while (
                    end < len(expression)
                    and expression[end].isascii()
                    and expression[end].isdigit()
                ):
                    end += 1
                number = int(expression[index:end])
                if number <= 0:
                    raise ValueError(
                        "Аргументы должны быть положительными целыми числами."
                    )
                values.push(number)
                index = end
                expect_value = False
            elif symbol in ("m", "M", "М"):
                if index + 1 >= len(expression) or expression[index + 1] != "(":
                    raise ValueError("После имени операции должна быть скобка '('.")
                name = "M" if symbol in ("M", "М") else "m"
                operations.push(Operation(name))
                index += 2
            else:
                raise ValueError("Ожидалось положительное число или операция m/M.")
        else:
            if symbol == ",":
                if operations.is_empty():
                    raise ValueError("Запятая находится вне операции.")
                operation = operations.peek()
                if operation.comma_found:
                    raise ValueError("У операции должны быть ровно два аргумента.")
                operation.comma_found = True
                expect_value = True
                index += 1
            elif symbol == ")":
                if operations.is_empty():
                    raise ValueError("Найдена лишняя закрывающая скобка.")
                operation = operations.pop()
                if not operation.comma_found:
                    raise ValueError("В операции отсутствует второй аргумент.")
                if len(values) < 2:
                    raise ValueError("Для вычисления недостаточно аргументов.")
                right = values.pop()
                left = values.pop()
                if operation.name == "m":
                    result = min(left, right)
                else:
                    result = max(left, right)
                values.push(result)
                index += 1
            else:
                raise ValueError("Ожидалась запятая или закрывающая скобка.")

    if expect_value:
        raise ValueError("Выражение обрывается: не хватает аргумента.")
    if not operations.is_empty():
        raise ValueError("Не все скобки закрыты.")
    if len(values) != 1:
        raise ValueError("Неверное количество значений в выражении.")
    return values.pop()
