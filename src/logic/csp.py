import numpy as np

class CSP:
    def __init__(self, board):
        """
        Initializes the CSP.
        :param board: A 9x9 numpy array (0 for empty cells).
        """
        self.board = board
        self.variables = self._get_variables()
        self.neighbors = self._get_neighbors()
        self.domains = self._get_domains()

    def _get_variables(self):
        """Returns a list of all cell coordinates (row, col)."""
        return [(r, c) for r in range(9) for c in range(9)]

    def _get_neighbors(self):
        """
        Generates neighbors for every variable based on Sudoku rules 
        (Row, Column, 3x3 Box) [cite: 49, 50, 51].
        """
        neighbors = {}
        for r in range(9):
            for c in range(9):
                peers = set()
                # Row and Column peers
                for k in range(9):
                    if k != c: peers.add((r, k))
                    if k != r: peers.add((k, c))
                
                # 3x3 Box peers
                box_r, box_c = (r // 3) * 3, (c // 3) * 3
                for i in range(box_r, box_r + 3):
                    for j in range(box_c, box_c + 3):
                        if (i, j) != (r, c):
                            peers.add((i, j))
                neighbors[(r, c)] = list(peers)
        return neighbors

    def _get_domains(self):
        """
        Initializes domains.
        Fixed cells: Domain is [value].
        Empty cells: Domain is [1..9][cite: 53, 54].
        """
        domains = {}
        for r in range(9):
            for c in range(9):
                if self.board[r, c] != 0:
                    domains[(r, c)] = [self.board[r, c]]
                else:
                    domains[(r, c)] = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        return domains
    
    def is_consistent(self, var, value, assignment):
        """Checks if assigning value to var conflicts with neighbors."""
        for neighbor in self.neighbors[var]:
            # Check against current assignment
            if neighbor in assignment and assignment[neighbor] == value:
                return False
            # Check against fixed board values (if any remained outside assignment)
            if self.board[neighbor] == value:
                 return False
        return True