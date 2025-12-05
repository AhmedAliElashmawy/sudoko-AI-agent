import numpy as np
import time
from csp import CSP
from ac3 import ac3
from backtracking import Backtracking


class SudokuSolver:
    def __init__(self, board=None):
        self.board = board
        self.steps_taken = 0
        self.method_used = ""
        self.board_states = []  # Store board states from AC3
        self.solve_time = 0.0  # Time taken to solve in seconds

    def solve(self, board=None, log_steps=False, log_file=None):
        """
        Solves the given Sudoku board (numpy array).
        Returns: (success, solved_board, method_description)
        
        Args:
            board: Sudoku puzzle as numpy array
            log_steps: If True, logs AC-3 execution details to file
            log_file: Path to log file (default: auto-generated timestamp)
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
        self.board_states = []  # Reset board states
        
        # Start timing
        start_time = time.time()
        
        csp = CSP(board)

        # Apply Arc Consistency
        ac3_success, self.board_states = ac3(csp, log_steps=log_steps, log_file=log_file)
        if not ac3_success:
            self.solve_time = time.time() - start_time
            self.method_used = "AC-3 Failed"
            print("fail")
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
            self.solve_time = time.time() - start_time
            self.method_used = "AC-3 Only"
            return True, board, self.method_used
    
    def get_board_states(self):
        """
        Returns the list of board states captured during AC-3 execution.
        Each state represents the board at a point when a domain became singleton.
        """
        return self.board_states
