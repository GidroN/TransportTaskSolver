from prettytable import PrettyTable
from copy import deepcopy
import random

class OpenTransportTaskError(Exception):
    pass


class TransportTaskSolver:
    def __init__(self, supply, demand, cost_elements=None):
        if sum(supply) != sum(demand):
            raise OpenTransportTaskError("Данная транспортная задача является открытой.\n Требования потребителей и ресурсы у поставщиков не сходятся.")
        self.supply = supply
        self.demand = demand
        self.cost_elements = cost_elements if cost_elements else None

    def _generate_matrix(self):
        demand_copy = self.demand.copy()
        supply_copy = self.supply.copy()

        matrix = [[] for _ in range(len(demand_copy) + 1)]
        matrix[0] = ['x0'] + [i for i in supply_copy]
        for i in range(1, len(demand_copy) + 1):
            matrix[i] = [demand_copy[i - 1]] + ['-' for i in range(len(supply_copy))]

        return matrix

    @staticmethod
    def _generate_table(matrix):
        for el in range(len(matrix[0])):
            if matrix[0].count(matrix[0][el]) > 1:
                matrix[0][el] = str(matrix[0][el]) + random.choice(['i', 'j', 'k', 'z', 'x', 'c'])

        result = matrix[0]
        matrix = matrix[1:]

        for i in range(len(matrix)):
            for j in range(len(matrix[0])):
                if matrix[i][j] == 0:
                    matrix[i][j] = '-'

        table = PrettyTable(result)
        table.add_rows(matrix)
        return table

    @staticmethod
    def _find_min_pos(matrix):
        i_pos, j_pos = 0, 0
        c = 10 ** 8
        for i in range(len(matrix)):
            for j in range(len(matrix[0])):
                if matrix[i][j] != 0 and matrix[i][j] < c:
                    c = matrix[i][j]
                    i_pos, j_pos = i, j
        return i_pos, j_pos

    @staticmethod
    def _count_matrix_elements(matrix):
        matrix_copy = deepcopy(matrix)
        matrix_copy = matrix_copy[1:]

        for i in matrix_copy:
            i.pop(0)

        count = 0
        for i in range(len(matrix_copy)):
            for j in range(len(matrix_copy[0])):
                if matrix_copy[i][j] != '-':
                    count += 1
        return True if count == len(matrix_copy) + len(matrix_copy[0]) - 1 else False

    def least_cost(self):
        demand_copy = self.demand.copy()
        supply_copy = self.supply.copy()
        cost_elements_copy = self.cost_elements.copy()

        demand_length = len(demand_copy)
        supply_length = len(supply_copy)
        result_matrix = self._generate_matrix()
        price_str, price = '', 0

        while True:
            cost_min = [['-' for _ in range(supply_length)] for _ in range(demand_length)]
            for i in range(demand_length):
                for j in range(supply_length):
                    cost_min[i][j] = cost_elements_copy[i][j] * min(demand_copy[i], supply_copy[j])

            i, j = self._find_min_pos(cost_min)
            res_el = int(min(demand_copy[i], supply_copy[j]))
            result_matrix[i + 1][j + 1] = res_el
            price_str += f"+{str(cost_min[i][j])}*{cost_elements_copy[i][j]}"
            price += int(cost_min[i][j])
            demand_copy[i] -= res_el
            supply_copy[j] -= res_el

            if self._count_matrix_elements(result_matrix):
                break

        print(self._generate_table(result_matrix))

        return f"Стоимость данного плана составляет: {price_str[1:]} = {price}"


    def north_west_corner(self):
        demand_copy = self.demand.copy()
        supply_copy = self.supply.copy()
        result_matrix = self._generate_matrix()

        i, j = 0, 0
        counter = 0
        while counter < len(self.supply) + len(self.demand) - 1:
            min_el = min(supply_copy[i], demand_copy[j])
            supply_copy[i] -= min_el
            demand_copy[j] -= min_el
            result_matrix[j + 1][i + 1] = min_el
            if supply_copy[i] == 0:
                i += 1
            elif demand_copy[j] == 0:
                j += 1
            counter += 1

        print(self._generate_table(result_matrix))

        if self.cost_elements:
            result_matrix = result_matrix[1:]

            for i in result_matrix:
                i.pop(0)

            price_str = ''
            price = 0
            for i in range(len(result_matrix)):
                for j in range(len(result_matrix[i])):
                    if result_matrix[i][j] != '-':
                        price += self.cost_elements[i][j] * result_matrix[i][j]
                        price_str += f'+{str(self.cost_elements[i][j])}*{str(result_matrix[i][j])}'

            return f"Стоимость данного плана составляет: {price_str[1:]} = {price}"

        else:
            return "Стоимость данного плана невозможно рассчитать, таблица стоимостей не указана."


def main():
    # supply = list(map(int, input("Введите поставщиков: ").split()))
    # demand = list(map(int, input("Введите потребителей: ").split()))
    supply = [100, 300, 300]
    demand = [100, 150, 250, 200]
    cost_elements = [[5, 2, 5],
                     [6, 1, 7],
                     [2, 5, 3],
                     [1, 7, 4]]
    # cost_elements = None

    prompt = input("Какой метод?(1 - мин. эл.; 2 - с.з. угол): ")
    if prompt == '1':
        task = TransportTaskSolver(supply, demand, cost_elements)
        print(task.least_cost())
    if prompt == '2':
        if cost_elements:
            task = TransportTaskSolver(supply, demand, cost_elements)
        else:
            task = TransportTaskSolver(supply, demand)
        print(task.north_west_corner())
    else:
        print("Выберите 1 или 2.")


if __name__ == '__main__':
    main()
