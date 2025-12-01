import numpy as np
from csp import CSP
from ac3 import ac3
from backtracking import BacktrackingSolver


class SudokuSolver:
    def __init__(self, board=None):
        self.board = board
        self.steps_taken = 0
        self.method_used = ""

    def solve(self, board=None):
        """
        Solves the given Sudoku board (numpy array).
        Returns: (success, solved_board, method_description)
        """
        if board is None:
            board = self.board
        
        if board is None:
            return False, None, "No board provided"
        
        # Convert to numpy if needed
        if isinstance(board, list):
            board = np.array(board, dtype=int)
        else:
            board = board.copy()
        
        self.steps_taken = 0
        csp = CSP(board)

        # Apply Arc Consistency
        if not ac3(csp):
            self.method_used = "AC-3 Failed"
            return False, board, self.method_used

        # Update grid with results from AC-3 (Singletons)
        ac3_solved_count = 0
        for r in range(9):
            for c in range(9):
                if len(csp.domains[(r, c)]) == 1:
                    if csp.board[r, c] == 0:
                        ac3_solved_count += 1
                    csp.board[r, c] = csp.domains[(r, c)][0]

        # Check if AC-3 alone solved it
        if all(len(csp.domains[var]) == 1 for var in csp.variables):
            for (r, c), val in csp.domains.items():
                board[r, c] = val[0]
            self.method_used = "AC-3 Only"
            return True, board, self.method_used

        # Run Backtracking to solve the rest
        initial_steps = self.steps_taken
        bt_solver = BacktrackingSolver()
        result_assignment = bt_solver.solve(None,randomize=False, use_csp=csp)
        
        # Count backtracking steps (approximate)
        empty_cells = sum(1 for var in csp.variables if len(csp.domains[var]) > 1)
        self.steps_taken = empty_cells
        
        if result_assignment:
            # Map assignment back to board array
            for (r, c), val in result_assignment.items():
                board[r, c] = val
            self.method_used = f"AC-3 + Backtracking ({self.steps_taken} steps)"
            return True, board, self.method_used
        else:
            self.method_used = "Backtracking Failed"
            return False, board, self.method_used
