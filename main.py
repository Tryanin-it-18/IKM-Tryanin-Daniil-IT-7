"""Текстовое меню индивидуального проекта: задания № 1 и № 17."""

from task1 import calculate_expression
from task17 import save_postman_result


def print_menu():
    print("\n" + "=" * 51)
    print(" ИНДИВИДУАЛЬНЫЙ ПРОЕКТ: ЗАДАНИЯ № 1 И № 17")
    print("=" * 51)
    print("1. Вычислить выражение с операциями m и M")
    print("2. Найти минимум извинений почтальона (из файла)")
    print("3. Показать примеры форматов")
    print("0. Выход")


def run_task1():
    print("\nОперация m(a,b) выбирает минимум, M(a,b) — максимум.")
    print("Используйте целые положительные числа без пробелов.")
    expression = input("Введите выражение: ")
    try:
        result = calculate_expression(expression)
        print(f"Результат: {result}")
    except ValueError as error:
        print(f"Ошибка ввода: {error}")


def run_task17():
    print("\nВ файле: M, затем M строк вида 'n_i l_i соседи...'.")
    filename = input("Путь к входному файлу: ").strip().strip('"')
    if not filename:
        print("Ошибка ввода: не указан путь к файлу.")
        return
    output_filename = input(
        "Имя выходного файла [postman_output.txt]: "
    ).strip().strip('"') or "postman_output.txt"
    try:
        result = save_postman_result(filename, output_filename)
        print(f"Минимальное количество извинений: {result}")
        print(f"Ответ записан в файл: {output_filename}")
    except ValueError as error:
        print(f"Ошибка ввода: {error}")


def show_examples():
    print("\nЗадание № 1: M(15,m(16,8))  ->  15")
    print("Задание № 17: examples/postman_example.txt  ->  2")
    print("Если PyCharm запускается из папки проекта, относительные пути работают.")


def main():
    while True:
        print_menu()
        choice = input("Выберите пункт меню: ").strip()
        if choice == "1":
            run_task1()
        elif choice == "2":
            run_task17()
        elif choice == "3":
            show_examples()
        elif choice == "0":
            print("Работа программы завершена.")
            return
        else:
            print("Ошибка: выберите 0, 1, 2 или 3.")


if __name__ == "__main__":
    main()
