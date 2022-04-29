

# def parse_factors(func: str, coef: int = 1) -> list:
#     func_factors = []
#     func = func.split()
#     for i in range(len(func)):
#         if "x_" in func[i]:
#             if func[i].find("x_") == 0:
#                 to_add = 1
#             else:
#                 to_add = int(func[i][:func[i].find("x_")])
#             func_factors.append(
#                 coef*to_add)
#             if (func[i-1] == "-"):
#                 func_factors[-1] *= -1
#     return func_factors


# input_ = ["F = 4x_1 + 5x_2 + 4x_3 -> max",
#           "2x_1 + 3x_2 + 6x_3 <= 240",
#           "4x_1 + 2x_2 + 4x_3 <= 200",
#           "4x_1 + 6x_2 + 8x_3 <= 160",
#           "x_1, x_2, x_3 >= 0"]


from termcolor import colored

# Находим те индексы которые относятся к базису ([0, 0, 1, 1, 1] -> [2, 3, 4])


def calc_basis_indexes(basis: list) -> list:
    return list(filter(lambda x: x != -1, map(lambda x: x if basis[x] else -1, range(len(basis)))))


# Считаем оценку, позволяющую понять, что следует ввести в базис или найдено ли оптимальное решение
def calculate_costs(function, basis, factors):
    costs = []
    basis_indexes = calc_basis_indexes(basis)
    for i in range(len(function)):
        subtotal = -function[i]
        for j in range(len(basis_indexes)):
            subtotal += function[basis_indexes[j]] * factors[j][i]
        costs.append(subtotal)
    return costs


# Дополняем наш вектор решений нулями
def extend_solutions(solutions, basis):
    res = list(solutions)
    for i in range(len(basis)):
        if basis[i] == 0:
            res.insert(i, 0)
    return res


# Тут должно быть очевидно
def dot_product(op1, op2):
    return [op1[i] * op2[i] for i in range(len(op1))]


# Какой-никакой, но форматированный вывод
def print_table(function, factors, basis, solutions, end=False):
    func = [f"{i:^11.2f}" for i in function]
    fact = [[f"{j:^11.2f}" for j in i] for i in factors]
    sols = extend_solutions(solutions, basis)
    sols.append(sum(dot_product(sols, function)))
    sols = [f"{i:^11.2f}" for i in sols]
    basis_indexes = calc_basis_indexes(basis)
    bas = [f"|  x{i+1:<3d} " for i in basis_indexes]
    separator = "+-------"+"+-----------"*(len(func)+1)+"+"
    costs = [f"{i:^11.2f}" for i in calculate_costs(
        function, basis, factors)]
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


# Данные
function = [4, 5, 4, 0, 0, 0]

factors = [[2, 3, 6, 1, 0, 0],
           [4, 2, 4, 0, 1, 0],
           [4, 6, 8, 0, 0, 1]]

basis = [0, 0, 0, 1, 1, 1]

solutions = [240, 200, 160]


print_table(function, factors, basis, solutions)
