import random
import numpy as np
from csp import CSP

class Backtracking:
    def __init__(self):
        self.steps = 0
    
    def btGenerate(self, board, randomize=False):
        """
         Generate a Sudoku board using backtracking.
        
        Args:
            board: 9x9 numpy array or list of lists
            randomize: If True, tries numbers in random order (for generation)
        
        Returns:
            True if solved (simple mode), assignment dict (CSP mode), or False/None on failure
        """
        # backtracking for generation
        # Convert to numpy if needed
        if isinstance(board, list):
            board = np.array(board, dtype=int)
        
        empty = self._find_empty(board)
        if not empty:
            return True  # Solved
        
        row, col = empty
        self.steps += 1
        
        nums = list(range(1, 10))
        if randomize:
            random.shuffle(nums)
        
        for num in nums:
            if self._is_valid(board, row, col, num):
                board[row, col] = num
                
                # Recur to continue solving
                if self.btGenerate(board, randomize):
                    return True
                
                # Backtrack
                board[row, col] = 0
        
        return False
    

    def countSolutions(self, board, max_solutions=2):
        """Count solutions up to max_solutions (default 2 for uniqueness check)."""
        empty = self._find_empty(board)
        if not empty:
            return 1
        
        row, col = empty
        count = 0
        for num in range(1, 10):
            if self._is_valid(board, row, col, num):
                board[row, col] = num
                
                count += self.countSolutions(board, max_solutions)

                board[row, col] = 0
                if count >= max_solutions:
                    return count
        return count

    def backtracking_search(self, board, randomize=False):
        """
        CSP-based backtracking search.
        Returns a complete assignment or None if failure.
        """
        # Create initial assignment from the current state of domains/board
        assignment = {}
        csp = CSP(board)
        for var in csp.variables:
            if len(csp.domains[var]) == 1:
                assignment[var] = csp.domains[var][0]
                
        return self._backtrack_csp(assignment, csp, randomize)
    
    def _backtrack_csp(self, assignment, csp, randomize):
        """Recursive backtracking function for CSP."""
        if len(assignment) == len(csp.variables):
            return assignment  # Solution found

        var = self._select_unassigned_variable(assignment, csp)
        
        # Order domain values
        domain_values = list(csp.domains[var])
        if randomize:
            random.shuffle(domain_values)
        
        for value in domain_values:
            if csp.is_consistent(var, value, assignment):
                assignment[var] = value
                self.steps += 1
                result = self._backtrack_csp(assignment, csp, randomize)
                if result:
                    return result
                del assignment[var]
                
        return None
    
    def _select_unassigned_variable(self, assignment, csp):
        """Selects the next variable to assign (Simple: first empty found)."""
        for var in csp.variables:
            if var not in assignment:
                return var
        return None
    
    def _find_empty(self, board):
        """Finds the first empty cell (0) in the board."""
        for r in range(9):
            for c in range(9):
                if board[r, c] == 0:
                    return (r, c)
        return None
    
    def _is_valid(self, board, row, col, num):
        """Checks if placing num at (row, col) is valid according to Sudoku rules."""
        # Check row
        if num in board[row]:
            return False
        
        # Check column
        if num in board[:, col]:
            return False
        
        # Check 3x3 box
        box_row, box_col = (row // 3) * 3, (col // 3) * 3
        if num in board[box_row:box_row+3, box_col:box_col+3]:
            return False
        
        return True