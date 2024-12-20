from functools import cached_property
from math import inf as infinity

class Cell:
    def __init__(self, row, col, data, grid):
        self.row = row
        self.col = col
        self.data = data
        self.grid = grid
        self.specialize()

    def __repr__(self):
        return f"({self.row},{self.col}):{self.data}"

    def specialize(self):
        """To fix data in subclass."""
        pass

    def init_astar(self):
        """To compute astar."""
        self.gscore = infinity
        self.fscore = infinity
        self.closed = False
        self.in_openset = False
        self.came_from = None

    @property
    def index(self):
        return f"({self.row},{self.col})"

    @property
    def rows(self):
        return self.grid.rows

    @property
    def cols(self):
        return self.grid.cols

    @property
    def part(self):
        return self.grid.part

    def print(self):
        return self.data

    def can_move(self, vector):
        new_row = self.row + vector[0]
        new_col = self.col + vector[1]

        if new_row < 0:
            return False
        # 10 rows : valid if new_row <= 9
        elif new_row + 1 > self.rows:
            return False
        elif new_col < 0:
            return False
        elif new_col + 1 > self.cols:
            return False
        else:
            return True

    def get_next(self, vector):
        if self.can_move(vector):
            row = self.row
            col = self.col
            row_delta = vector[0]
            col_delta = vector[1]
            cell = self.grid.data[row+row_delta][col+col_delta]
            return cell
        else:
            return None
    
    @cached_property
    def right_cell(self):
        return self.get_next((0, 1))

    @cached_property
    def left_cell(self):
        return self.get_next((0, -1))

    @cached_property
    def up_cell(self):
        return self.get_next((-1, 0))

    @cached_property
    def down_cell(self):
        return self.get_next((1, 0))

    def manhattan_distance(self, destination):
        return abs(self.row - destination.row) + abs(self.col - destination.col)

    @property
    def path_neighbors(self):
        raise NotImplementedError("Todo in subclass for path calculation")

    def cost_to_neighbor(self, neighbor, path):
        raise NotImplementedError("Todo in subclass for path calculation")

    def neighbors(self, inline=True, diagonals=False, fullline=False):
        """Return all neighbors

        Default : only adjacent in line
        Option :
            diagonals : include diagnoles
            fullline : include all line
        """

        neighbors = []
        vectors = []

        if inline:
            vectors.append((-1,0))
            vectors.append((1,0))
            vectors.append((0,1))
            vectors.append((0,-1))

        if diagonals:
            vectors.append((-1,-1))
            vectors.append((-1,1))
            vectors.append((1,-1))
            vectors.append((1,1))

        for vector in vectors:
            cell = self.get_next(vector)
            if cell is not None:
                neighbors.append(cell)
                if fullline:
                    delta = 2
                    while cell is not None:
                        new_vector = [item * delta for item in vector]
                        cell = self.get_next(new_vector)
                        delta += 1
                        if cell:
                            neighbors.append(cell)
        return neighbors



class Grid:
    def __init__(self, data, part=1, cell_obj=Cell):
        self.raw_data = data
        self.data = []
        self.part = part

        for row_index, cols in enumerate(data):
            row = []
            for col_index, cell_data in enumerate(cols):
                cell = cell_obj(row_index, col_index, cell_data, self)
                row.append(cell)
            self.data.append(row)

    @property
    def rows(self):
        return len(self.data)

    @property
    def cols(self):
        return len(self.data[0])

    @property
    def nb_cells(self):
        return self.rows * self.cols

    @property
    def cells(self):
        for row in self.data:
            for cell in row:
                yield cell

    def __repr__(self):
        lines = []
        for row in self.data:
            line = ''.join(list(map(lambda x: x.print(), row)))
            lines.append(line)
        return "\n".join(lines)

    def get_cell(self, row, col):
        return self.data[row][col]

    def manhattan_distance(self, source, destination):
        return source.manhattan_distance(destination)

    def compute_best_path(self, start, end):
        """
        Compute a the best path from start to end.
        Cell need to have a function cost_to_neighbor to compute cost.
        """

        # queue
        q = [
            # cost, start, path
            (0, start, []),
        ]
        mins = {start: 0}
        min_path = None
        best_path = None
        while q:
            (cost, cell, path) = q.pop(0)
            if min_path is not None and min_path < cost:
                continue

            path = [cell] + path
            if cell == end:
                if min_path is None:
                    min_path = cost
                    best_path = path
                elif min_path > cost:
                    min_path = cost
                    best_path = path
            else:
                for neighbor in cell.path_neighbors:
                    if neighbor in path:
                        continue
                    prev_cost = mins.get(neighbor, None)

                    cost_to_neighbor = cell.cost_to_neighbor(neighbor, path)
                    next_cost = cost + cost_to_neighbor

                    if prev_cost is None or next_cost < prev_cost:
                        mins[neighbor] = next_cost
                        q.append((next_cost, neighbor, path))

        if best_path is not None:
            self.best_path = list(reversed(best_path))
            self.best_path_mins = mins
        else:
            self.best_path = None
            self.best_path_mins = {}
        self.best_path_cost = min_path
