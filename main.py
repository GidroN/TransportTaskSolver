from prettytable import PrettyTable


class OpenTransportTaskError(Exception):
    pass


class TransportTaskSolver:
    def __init__(self, supply, demand, cost_elements=None):
        if sum(supply) != sum(demand):
            raise OpenTransportTaskError(
                "Данная транспортная задача является открытой.\n Требования потребителей и ресурсы у поставщиков не сходятся.")
        self.supply = supply
        self.demand = demand
        self.cost_elements = cost_elements if cost_elements else None

    def _generate_matrix(self):
        demand_copy = self.demand.copy()
        supply_copy = self.supply.copy()

        bfs = [[] for _ in range(len(demand_copy) + 1)]
        bfs[0] = ['x0'] + [i for i in supply_copy]
        for i in range(1, len(demand_copy) + 1):
            bfs[i] = [demand_copy[i - 1]] + ['-' for i in range(len(supply_copy))]

        return bfs

    @staticmethod
    def _generate_table(matrix):
        first_elements = matrix[0]
        result = matrix[1:]
        table = PrettyTable(first_elements)
        table.add_rows(result)
        return table

    def least_cost(self):
        """In Progress..."""
        pass

    def north_west_corner(self):
        demand_copy = self.demand.copy()
        supply_copy = self.supply.copy()
        bfs = self._generate_matrix()

        i, j = 0, 0
        counter = 0
        while counter < len(self.supply) + len(self.demand) - 1:
            min_el = min(supply_copy[i], demand_copy[j])
            supply_copy[i] -= min_el
            demand_copy[j] -= min_el
            bfs[j + 1][i + 1] = min_el
            if supply_copy[i] == 0 and i < len(self.supply) - 1:
                i += 1
            elif demand_copy[j] == 0 and j < len(self.demand) - 1:
                j += 1
            counter += 1

        print(self._generate_table(bfs))

        if self.cost_elements:
            result = bfs[1:]

            for i in result:
                i.pop(0)

            string = ''
            cost = 0
            for i in range(len(result)):
                for j in range(len(result[i])):
                    if result[i][j] != '-':
                        cost += self.cost_elements[i][j] * result[i][j]
                        string += f'+{str(self.cost_elements[i][j])}*{str(result[i][j])}'

            return f"Стоимость данного плана составляет: {string[1:]} = {cost}"

        else:
            return "Стоимость данного плана невозможно рассчитать, таблица стоимостей не указана."


def main():
    # supply = list(map(int, input("Введите поставщиков: ").split()))
    # demand = list(map(int, input("Введите потребителей: ").split()))
    supply = [120, 50, 130]
    demand = [100, 100, 100]
    cost_elements = [[2, 5, 1],
                     [3, 2, 6],
                     [7, 2, 5]]
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
