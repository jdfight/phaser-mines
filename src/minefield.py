import random
from .cell import Cell

class Minefield:
    """
    Manages the game's grid, mine placement, and core logic.
    """
    def __init__(self, width, height, num_mines):
        self.width = width
        self.height = height
        self.num_mines = num_mines
        self.flags_placed = 0
        self.grid = [[Cell(x, y) for x in range(width)] for y in range(height)]
        self.game_over = False
        self.game_won = False
        self._generate_board()

    @property
    def mines_remaining(self):
        return self.num_mines - self.flags_placed

    def _generate_board(self):
        """
        Generates a new board, placing mines and calculating numbers.
        """
        # Place mines
        mine_positions = random.sample(range(self.width * self.height), self.num_mines)
        for pos in mine_positions:
            x = pos % self.width
            y = pos // self.width
            self.grid[y][x].is_mine = True

        # Calculate adjacent mines for each cell
        for y in range(self.height):
            for x in range(self.width):
                if not self.grid[y][x].is_mine:
                    self.grid[y][x].adjacent_mines = self._count_adjacent_mines(x, y)

    def _count_adjacent_mines(self, x, y):
        """Counts mines in the 8 neighboring cells."""
        count = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                nx, ny = x + j, y + i
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    if self.grid[ny][nx].is_mine:
                        count += 1
        return count

    def open_cell(self, x, y):
        """
        Opens a cell and handles the consequences.
        Returns a list of updated cells.
        """
        if self.game_over:
            return []

        cell = self.grid[y][x]
        if cell.is_open or cell.is_flagged:
            return []

        cell.is_open = True
        updated_cells = [cell]

        if cell.is_mine:
            self.game_over = True
            self.game_won = False
            # In a real game, you might want to reveal all mines here
            return updated_cells

        if cell.adjacent_mines == 0:
            updated_cells.extend(self._flood_fill(x, y))

        self._check_win_condition()
        return updated_cells

    def _flood_fill(self, x, y):
        """
        Recursively opens adjacent cells if the current cell is empty.
        """
        updated_cells = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                nx, ny = x + j, y + i
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    if not self.grid[ny][nx].is_open and not self.grid[ny][nx].is_flagged:
                        # Recursively call open_cell, but we just need the logic
                        # so we call parts of it manually to avoid re-checking game over
                        neighbor = self.grid[ny][nx]
                        neighbor.is_open = True
                        updated_cells.append(neighbor)
                        if neighbor.adjacent_mines == 0:
                            updated_cells.extend(self._flood_fill(nx, ny))
        return updated_cells

    def toggle_flag(self, x, y):
        """Toggles a flag on a cell."""
        if self.game_over:
            return None

        cell = self.grid[y][x]
        if not cell.is_open:
            cell.is_flagged = not cell.is_flagged
            if cell.is_flagged:
                self.flags_placed += 1
            else:
                self.flags_placed -= 1
            return cell
        return None

    def _check_win_condition(self):
        """Checks if the game has been won."""
        open_cells = 0
        for y in range(self.height):
            for x in range(self.width):
                if self.grid[y][x].is_open:
                    open_cells += 1

        if open_cells == (self.width * self.height) - self.num_mines:
            self.game_over = True
            self.game_won = True

    def __repr__(self):
        return f"Minefield({self.width}x{self.height}, {self.num_mines} mines)"
