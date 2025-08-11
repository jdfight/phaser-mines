class Cell:
    """
    Represents a single cell in the minefield.
    """
    def __init__(self, x, y, is_mine=False):
        self.x = x
        self.y = y
        self.is_mine = is_mine
        self.is_open = False
        self.is_flagged = False
        self.adjacent_mines = 0

    def __repr__(self):
        return f"Cell({self.x}, {self.y}, mine={self.is_mine}, open={self.is_open})"
