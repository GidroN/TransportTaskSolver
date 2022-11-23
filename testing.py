from prettytable import PrettyTable


def _generate_table(matrix):
    first_elements = matrix[0]
    result = matrix[1:]
    table = PrettyTable(first_elements)
    table.add_rows(result)
    return table


def find_min_pos(matrix):
    c = 10 ** 8
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if matrix[i][j] != 0 and matrix[i][j] < c:
                c = matrix[i][j]
                i_pos, j_pos = i, j
    return i_pos, j_pos


def count_matrix_elements(matrix):
    count = 0
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if matrix[i][j] != '-':
                count += 1
    return True if count == len(matrix) + len(matrix[0]) - 1 else False


def least_cost(demand, supply, costs):
    demand_copy = demand.copy()
    supply_copy = supply.copy()
    costs_copy = costs.copy()

    demand_length = len(demand_copy)
    supply_length = len(supply_copy)
    result_matrix = [['-' for _ in range(demand_length)] for _ in range(supply_length)]
    price_str, price = '', 0

    while True:
        # for i in range(demand_length):
        #     for j in range(supply_length):
        #         cost_min[i][j] = (costs_copy[i][j] * min(demand_copy[i], supply_copy[j]))

        i, j = find_min_pos(costs_copy)
        costs_copy[i][j] = 10 ** 8
        res_el = int(min(demand_copy[i], supply_copy[j]))
        result_matrix[i][j] = res_el
        print(result_matrix)
        price_str += f"+{str(costs_copy[i][j])}"
        price += int(costs_copy[i][j])
        demand_copy[i] -= res_el
        supply_copy[j] -= res_el

        if count_matrix_elements(result_matrix):
            break


    # print(_generate_table(result_matrix))
    table = PrettyTable()
    table.add_rows(result_matrix)
    print(table)

    return f"Стоимость данного плана составляет: {price_str[1:]} = {price}"


supply = [120, 50, 130]
demand = [100, 100, 100]
costs = [[2, 5, 1],
         [3, 2, 6],
         [7, 2, 5]]

print(least_cost(demand, supply, costs))
