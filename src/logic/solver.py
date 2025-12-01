import numpy as np
from csp import CSP
from ac3 import ac3
from backtracking import backtracking_search

class SudokuSolver:
    def __init__(self):
        pass

    def solve(self, board):
        """
        Solves the given Sudoku board (numpy array).
        Returns: (True, solved_board) or (False, original_board)
        """
        csp = CSP(board)

        # 2. Apply Arc Consistency [cite: 55]
        if not ac3(csp):
            print("No solution found (AC-3 inconsistency).")
            return False, board

        # 3. Update grid with results from AC-3 (Singletons) [cite: 59, 60]
        for r in range(9):
            for c in range(9):
                if len(csp.domains[(r, c)]) == 1:
                    csp.board[r, c] = csp.domains[(r, c)][0]

        # 4. Run Backtracking to solve the rest 
        result_assignment = backtracking_search(csp)
        
        if result_assignment:
            # Map assignment back to board array
            for (r, c), val in result_assignment.items():
                board[r, c] = val
            return True, board
        else:
            print("No solution found (Backtracking failure).")
            return False, board

    def generate_random_puzzle(self):
        """
        Generates a solvable random puzzle (required by assignment ).
        """
        # Start with empty board
        empty_board = np.zeros((9, 9), dtype=int)
        csp = CSP(empty_board)
        
        # Fill diagonal 3x3 boxes randomly (this is valid and safe)
        for k in range(0, 9, 3):
            nums = np.arange(1, 10)
            np.random.shuffle(nums)
            idx = 0
            for i in range(3):
                for j in range(3):
                    csp.domains[(k+i, k+j)] = [nums[idx]]
                    csp.board[k+i, k+j] = nums[idx]
                    idx += 1

        # Run backtracking to fill the rest
        full_solution = backtracking_search(csp)
        
        # Create puzzle by removing elements from the full solution
        final_board = np.zeros((9, 9), dtype=int)
        for (r, c), val in full_solution.items():
            final_board[r, c] = val
            
        # Remove random cells to create the puzzle
        # (Removing ~40-50 cells typically creates a playable puzzle)
        attempts = 45 
        while attempts > 0:
            r, c = np.random.randint(0, 9), np.random.randint(0, 9)
            if final_board[r, c] != 0:
                final_board[r, c] = 0
                attempts -= 1
                
        return final_board