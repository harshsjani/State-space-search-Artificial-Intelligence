import os
from collections import deque


class Constants:
    input_filename = "input.txt"
    output_filename = "output.txt"
    fail_output = "FAIL"
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]


class Solver:
    def __init__(self):
        self.parse_input()
        self.paths_to_settling_sites = [None for _ in range(self.num_settling_sites)]
        self.serialized_output = []
        self.calls = {"BFS": self.bfs, "UCS": self.ucs, "A*": self.a_star}
    
    def parse_input(self):
        cwd = os.getcwd()
        input_file_path = os.path.join(cwd, Constants.input_filename)

        with open(input_file_path, 'r') as file:
            self.algo = file.readline().strip("\n")
            self.num_cols, self.num_rows = map(int, file.readline().split())
            self.starting_x, self.starting_y = map(int, file.readline().split())
            self.max_rock_height = int(file.readline())
            self.num_settling_sites = int(file.readline())

            self.settling_sites = []

            for _ in range(self.num_settling_sites):
                self.settling_sites.append((map(int, file.readline().split())))

            self.grid = [[0 for _ in range(self.num_cols)] for _ in range(self.num_rows)]

            for idx in range(self.num_rows):
                col_vals = map(int, file.readline().split())
                
                for widx, val in enumerate(col_vals):
                    self.grid[idx][widx] = val

    def serialize_outputs(self):
        for path in self.paths_to_settling_sites:
            if path is None:
                self.serialized_output.append(Constants.fail_output)
            else:
                self.serialized_output.append(" ".join(["%s,%s" % cell for cell in path]))

    def write_output(self):
        cwd = os.getcwd()
        output_file_path = os.path.join(cwd, Constants.output_filename)
        self.serialize_outputs()

        with open(output_file_path, "w") as file:
            file.writelines('\n'.join(self.serialized_output))


    def show_input(self):
        print("Algorithm: %s\nW H: %d %d\nStarting Position: %d %d\nMaximum Rock Height Difference: %d\nNumber of Settling Sites: %d\nSettling Sites: %s" % (
            self.algo, self.num_cols, self.num_rows, self.starting_x, self.starting_y, self.max_rock_height, self.num_settling_sites, self.settling_sites
        ))

        print("\nGrid:")
        for row in self.grid:
            print(row)

    def get_valid_neighbors(self, x, y):
        neighbors = []
        
        for i, j in Constants.directions:
            p = x + i
            q = y + j

            cost = 14 if abs(i) == abs(j) else 10

            if 0 <= p < self.num_cols and 0 <= q < self.num_rows:
                cur_height = self.grid[y][x]
                new_height = self.grid[q][p]

                height_dif = 0

                if cur_height < 0:
                    if new_height < 0:
                        height_dif = abs(cur_height - new_height)
                    else:
                        height_dif = abs(cur_height)
                elif new_height < 0:
                    height_dif = abs(new_height)

                if height_dif <= self.max_rock_height:
                    neighbors.append((p, q, cost))
        return neighbors

    def bfs(self):
        sx, sy = self.starting_x, self.starting_y
        
        open = deque()
        open.append((sx, sy))
        visited = set([sx, sy])

        parentpointer = {}

        while open:
            temp = deque()
            while open:
                nx, ny = open.popleft()

                for p, q, _ in self.get_valid_neighbors(nx, ny):
                    if (p, q) not in visited:
                        visited.add((p, q))
                        parentpointer[(p, q)] = (nx, ny)
                        temp.append((p, q))
            open = temp
        
        for idx, (x, y) in enumerate(self.settling_sites):
            path = []
            if (x, y) not in parentpointer:
                continue

            while (x, y) != (sx, sy):
                path.append((x, y))
                x, y = parentpointer[(x, y)]
            
            path.append((sx, sy))
            self.paths_to_settling_sites[idx] = reversed(path)

    def ucs(self):
        print("SOLVING UCS")

    def a_star(self):
        print("SOLVING A*!")

    def solve(self):
        self.calls[self.algo]()


def main():
    solver = Solver()
    solver.solve()
    solver.write_output()
    # solver.show_input()


if __name__ == "__main__":
    main()
