"""Комплексные тесты заданий № 1 и № 17 без внешних библиотек."""

import heapq
import os
import random
import tempfile
import unittest

from structures import Stack
from task1 import calculate_expression
from task17 import read_tree, save_postman_result, solve_postman


class StackTests(unittest.TestCase):
    def test_push_pop_lifo(self):
        stack = Stack()
        stack.push(1)
        stack.push(3)
        self.assertEqual(stack.pop(), 3)
        self.assertEqual(stack.pop(), 1)
        self.assertTrue(stack.is_empty())

    def test_empty_stack(self):
        stack = Stack()
        with self.assertRaises(ValueError):
            stack.pop()


class ExpressionTests(unittest.TestCase):
    def test_example(self):
        self.assertEqual(calculate_expression("M(15,m(16,8))"), 15)

    def test_minimum(self):
        self.assertEqual(calculate_expression("m(12,7)"), 7)

    def test_maximum(self):
        self.assertEqual(calculate_expression("M(12,7)"), 12)

    def test_complex_nested(self):
        self.assertEqual(calculate_expression("m(M(15,3),M(m(2,4),8))"), 8)

    def test_deep_nesting(self):
        expression = "1"
        for index in range(40):
            expression = f"M({expression},2)"
        self.assertEqual(calculate_expression(expression), 2)

    def test_equal_arguments(self):
        self.assertEqual(calculate_expression("m(5,5)"), 5)

    def test_large_arguments(self):
        self.assertEqual(calculate_expression("M(100000000000,999)"), 100000000000)

    def test_cyrillic_capital_m(self):
        self.assertEqual(calculate_expression("М(11,5)"), 11)

    def test_plain_number(self):
        self.assertEqual(calculate_expression("6"), 6)

    def test_empty_expression(self):
        with self.assertRaises(ValueError):
            calculate_expression("")

    def test_missing_bracket(self):
        with self.assertRaises(ValueError):
            calculate_expression("m(1,2")

    def test_missing_second_argument(self):
        with self.assertRaises(ValueError):
            calculate_expression("m(1,)")

    def test_extra_argument(self):
        with self.assertRaises(ValueError):
            calculate_expression("m(1,2,3)")

    def test_zero(self):
        with self.assertRaises(ValueError):
            calculate_expression("M(0,2)")

    def test_spaces(self):
        with self.assertRaises(ValueError):
            calculate_expression("m(1, 2)")

    def test_unknown_character(self):
        with self.assertRaises(ValueError):
            calculate_expression("m(3,4)*2")


class PostmanTests(unittest.TestCase):
    def write_temp(self, content):
        with tempfile.NamedTemporaryFile(
            "w", encoding="utf-8", delete=False, suffix=".txt"
        ) as stream:
            stream.write(content)
            self.addCleanup(lambda: os.path.exists(stream.name) and os.remove(stream.name))
            return stream.name

    def test_official_example(self):
        path = os.path.join(os.path.dirname(__file__), "..", "examples", "postman_example.txt")
        self.assertEqual(solve_postman(path), 2)

    def test_single_nest_with_mail(self):
        self.assertEqual(solve_postman(self.write_temp("1\n0 5\n")), 0)

    def test_single_nest_without_mail(self):
        self.assertEqual(solve_postman(self.write_temp("1\n0 0\n")), 0)

    def test_no_letters(self):
        self.assertEqual(solve_postman(self.write_temp("2\n1 0 2\n1 0 1\n")), 0)

    def test_path_with_one_mail(self):
        data = "4\n1 0 2\n2 0 1 3\n2 0 2 4\n1 2 3\n"
        self.assertEqual(solve_postman(self.write_temp(data)), 3)

    def test_unneeded_leaf(self):
        data = "3\n2 0 2 3\n1 1 1\n1 0 1\n"
        self.assertEqual(solve_postman(self.write_temp(data)), 1)

    def test_star_with_mail(self):
        data = "4\n3 0 2 3 4\n1 1 1\n1 1 1\n1 1 1\n"
        self.assertEqual(solve_postman(self.write_temp(data)), 3)

    def test_output_file(self):
        input_path = self.write_temp("1\n0 1\n")
        with tempfile.TemporaryDirectory() as temp_dir:
            result_path = os.path.join(temp_dir, "answer.txt")
            self.assertEqual(save_postman_result(input_path, result_path), 0)
            with open(result_path, encoding="utf-8") as file:
                self.assertEqual(file.read(), "0\n")

    def test_file_not_found(self):
        with self.assertRaises(ValueError):
            solve_postman("this_file_does_not_exist_987654.txt")

    def test_empty_file(self):
        with self.assertRaises(ValueError):
            solve_postman(self.write_temp(""))

    def test_bad_degree(self):
        with self.assertRaises(ValueError):
            solve_postman(self.write_temp("2\n2 1 2\n1 0 1\n"))

    def test_nonsymmetric_edges(self):
        with self.assertRaises(ValueError):
            solve_postman(self.write_temp("3\n2 1 2 3\n1 0 1\n1 0 2\n"))

    def test_cycle_and_disconnected(self):
        with self.assertRaises(ValueError):
            solve_postman(self.write_temp(
                "4\n2 1 2 3\n2 0 1 3\n2 0 1 2\n0 0\n"
            ))

    def test_negative_mail(self):
        with self.assertRaises(ValueError):
            solve_postman(self.write_temp("1\n0 -1\n"))

    def test_extra_lines(self):
        with self.assertRaises(ValueError):
            solve_postman(self.write_temp("1\n0 1\n0 1\n"))

    def test_random_small_trees_against_independent_search(self):
        """Дейкстра по (гнездо, набор обслуженных адресатов) для малых деревьев."""
        generator = random.Random(1701)
        for size in range(2, 9):
            for _ in range(45):
                adjacency = [[] for i in range(size)]
                for new in range(1, size):
                    parent = generator.randrange(new)
                    adjacency[new].append(parent)
                    adjacency[parent].append(new)
                letters = [generator.randrange(4) for _ in range(size)]
                lines = [str(size)]
                for node in range(size):
                    row = [len(adjacency[node]), letters[node]]
                    row += [neighbor + 1 for neighbor in adjacency[node]]
                    lines.append(" ".join(map(str, row)))
                actual = solve_postman(self.write_temp("\n".join(lines) + "\n"))
                expected = brute_minimum(adjacency, letters)
                self.assertEqual(actual, expected, (size, adjacency, letters))


def brute_minimum(adjacency, letters):
    targets = [i for i, amount in enumerate(letters) if amount > 0]
    if not targets:
        return 0
    position = {node: index for index, node in enumerate(targets)}
    all_visited = (1 << len(targets)) - 1
    start_mask = 1 << position[0] if 0 in position else 0
    start_cost = 0 if start_mask else 1
    priority = [(start_cost, 0, start_mask)]
    best = {(0, start_mask): start_cost}
    while priority:
        cost, node, visited = heapq.heappop(priority)
        if cost != best[(node, visited)]:
            continue
        if visited == all_visited:
            return cost
        for next_node in adjacency[node]:
            letter_bit = 1 << position[next_node] if next_node in position else 0
            new_visited = visited | letter_bit
            addition = 0 if letter_bit and not (visited & letter_bit) else 1
            new_cost = cost + addition
            state = (next_node, new_visited)
            if new_cost < best.get(state, float("inf")):
                best[state] = new_cost
                heapq.heappush(priority, (new_cost, next_node, new_visited))
    raise AssertionError("Программа независимой проверки не нашла маршрут")


if __name__ == "__main__":
    unittest.main()
