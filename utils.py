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

    def __repr__(self):
        lines = []
        for row in self.data:
            line = ''.join(list(map(lambda x: x.print(), row)))
            lines.append(line)
        return "\n".join(lines)
