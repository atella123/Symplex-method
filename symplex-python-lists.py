from numbers import Number
from typing import Tuple
from termcolor import colored
import numpy as np

# Находим те индексы которые относятся к базису ([0, 0, 1, 1, 1] -> [2, 3, 4])


def calc_basis_indexes(basis: list) -> list:
    return list(filter(lambda x: x != -1, map(lambda x: x if basis[x] else -1, range(len(basis)))))


# Считаем оценку, позволяющую понять, что следует ввести в базис или найдено ли оптимальное решение
def calculate_costs(function: list[Number], basis: list[Number], factors: list[list[Number]]) -> list[Number]:
    costs = []
    basis_indexes = calc_basis_indexes(basis)
    for i in range(len(function)):
        subtotal = -function[i]
        for j in range(len(basis_indexes)):
            subtotal += function[basis_indexes[j]] * factors[j][i]
        costs.append(subtotal)
    return costs


def index_of_min(in_: list) -> int:
    return in_.index(min(in_))


def index_of_min_positive(in_: list) -> int:
    max_ = max(in_)
    return index_of_min([max_ if i < 0 else i for i in in_])


# Ищем какой элемент следует убрать из базиса
def find_index_to_remove(index_to_add: int, factors: list, solutions: list) -> int:
    min_value = 0
    min_index = 0
    while not min_value:
        if factors[min_index][index_to_add] > 0:
            min_value = solutions[min_index] / factors[min_index][index_to_add]
        min_index += 1
    min_index -= 1
    for i in range(min_index, len(solutions)):
        if factors[i][index_to_add]:
            value = solutions[i] / factors[i][index_to_add]
            if value < min_value and value > 0:
                min_value = value
                min_index = i
    return min_index


# Меняем базис
def change_basis(index_to_add: int, index_to_remove: int, basis: list[int], factors: list[list[int]], solutions: list[int]) -> Tuple[list, list, list]:
    new_factors = []
    new_solutions = []
    basis[calc_basis_indexes(basis)[index_to_remove]] = 0
    basis[index_to_add] = 1
    new_index_position = basis[:index_to_add].count(1)
    solutions[index_to_remove] /= factors[index_to_remove][index_to_add]
    factors[index_to_remove] = [i / factors[index_to_remove][index_to_add]
                                for i in factors[index_to_remove]]
    for i in range(len(factors)):
        if i != index_to_remove:
            new_factors.append([factors[i][j] - factors[index_to_remove]
                               [j] * factors[i][index_to_add] for j in range(len(factors[i]))])
            new_solutions.append(solutions[i] - solutions[index_to_remove]
                                 * factors[i][index_to_add])
    new_solutions.insert(new_index_position, solutions[index_to_remove])
    new_factors.insert(new_index_position, factors[index_to_remove])
    return new_factors, new_solutions, basis


def extend_solutions(solutions: list[float], basis: list[float]) -> list[float]:
    res = []
    j = 0
    for i in range(len(basis)):
        if basis[i]:
            res.append(solutions[j])
            j += 1
        else:
            res.append(0)
    return res


def dot_product(op1: list[float], op2: list[float]) -> list[float]:
    return [op1[i] * op2[i] for i in range(len(op1))]


def next_iteration(function_to_maximize, factors, basis, solutions):
    return change_basis(index_of_min(calculate_costs(function_to_maximize, basis, factors)), find_index_to_remove(index_of_min(calculate_costs(
        function_to_maximize, basis, factors)), factors, solutions), basis, factors, solutions)


def solve(function_to_maximize, factors, basis, solutions, printing=False):
    while any(map(lambda x: x < 0, calculate_costs(function_to_maximize, basis, factors))):
        if printing:
            print_table(function_to_maximize, factors, basis, solutions)
        factors, solutions, basis = next_iteration(
            function_to_maximize, factors, basis, solutions)
    if printing:
        print_table(function_to_maximize, factors, basis, solutions, True)
    return extend_solutions(solutions, basis)


def print_table(function_to_maximize, factors, basis, solutions, end=False):
    func = [f"{i:^11.2f}" for i in function_to_maximize]
    fact = [[f"{j:^11.2f}" for j in i] for i in factors]
    sols = extend_solutions(solutions, basis)
    sols.append(sum(dot_product(extend_solutions(
        solutions, basis), function_to_maximize)))
    sols = [f"{i:^11.2f}" for i in sols]
    basis_indexes = calc_basis_indexes(basis)
    bas = [f"|  x{i+1:<3d} " for i in basis_indexes]
    separator = "+-------"+"+-----------"*(len(func)+1)+"+"
    costs = [f"{i:^11.2f}" for i in calculate_costs(
        function_to_maximize, basis, factors)]
    print(separator)
    print("|   f   =" + "+".join(func) + "=" +
          colored(sols[-1], "green" if end else 'red')+"|")
    print("|  x =  (" + ",".join(sols[:-1]) + ")" + "           |")
    print(separator)
    print("|      ", *
          [f"|    x{i+1:<5d}" for i in range(len(func))], "|           |")
    for i in range(len(fact)):
        print(bas[i], *fact[i], sols[basis_indexes[i]], sep="|", end="|\n")
    print(separator)
    print("|   Δ   ", *costs, "           ", sep="|", end="|\n")
    print(separator)


if __name__ == "__main__":
    function_to_maximize = [4, 5, 4, 0, 0, 0]
    factors = [[2, 3, 6, 1, 0, 0],
               [4, 2, 4, 0, 1, 0],
               [4, 6, 8, 0, 0, 1]]
    solutions = [240, 200, 160]
    basis = [0, 0, 0, 1, 1, 1]

    solve(function_to_maximize, factors, basis, solutions, True)
