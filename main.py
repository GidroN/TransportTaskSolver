class TransportTaskSolver:
    def __init__(self, matrix):
        self.matrix = matrix

    def min_element(self):
        pass

    def northwest(self):
        pass


def main():
    matrix = input("Укажите матрицу: ")
    task = TransportTaskSolver(matrix)
    prompt = input("Какой метод?(1 - мин. эл.; 2 - с.з. угол): ")
    if prompt == '1':
        return task.min_element()
    else:
        return task.northwest()


if __name__ == '__main__':
    main()
