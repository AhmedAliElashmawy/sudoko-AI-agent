import copy
import random
import numpy as np
from backtracking import BacktrackingSolver
from solver import SudokuSolver


class SudokuGenerator:
    """
    Generates puzzles by:
    1. Creating a full valid board.
    2. Removing numbers.
    3. Verifying difficulty using the Solver.
    """
    @staticmethod
    def generate(difficulty="Medium"):
        """
        Generate a Sudoku puzzle with specified difficulty.
        
        Args:
            difficulty: "Easy", "Medium", or "Hard"
        
        Returns:
            A 9x9 numpy array representing the puzzle (0 for empty cells)
        """
        # Difficulty Map: (Target Clues to Remove, Minimum Backtrack Steps)
        settings = {
            "Easy": (30, 0),      # Few removed, AC3 should solve it (0 steps)
            "Medium": (45, 10),   # More removed, Backtrack needed but shallow
            "Hard": (54, 100)     # Many removed, Deep backtrack needed
        }
        
        target_removal, min_steps = settings.get(difficulty, (40, 10))
        best_board = None
        
        for _ in range(20):
            # 1. Create Full Board
            board = np.zeros((9, 9), dtype=int)
            bt = BacktrackingSolver()
            bt.solve(board, randomize=True)  # Random valid board
            
            # 2. Remove Numbers
            puzzle = SudokuGenerator._remove_cells(board, target_removal)
            
            # 3. Test Difficulty
            solver = SudokuSolver(puzzle)
            success, board_solution, method = solver.solve()
            
            steps = solver.steps_taken
            
            # 4. Check Criteria
            if difficulty == "Easy" and "AC-3 Only" in method:
                return puzzle, board_solution, success, method
            elif difficulty == "Medium" and steps > 0 and steps < 100:
                return puzzle, board_solution, success, method
            elif difficulty == "Hard" and steps >= 50:  # 50 is a reasonable hard floor
                return puzzle, board_solution, success, method
                
            best_board = puzzle  # Keep checking
        # Return best effort if exact criteria not met
        if best_board is not None:
            return best_board, board_solution, success, method
        else:
            return SudokuGenerator._fallback_generate(target_removal)

    @staticmethod
    def _remove_cells(board, count):
        """Remove specified number of cells from the board."""
        puzzle = copy.deepcopy(board)
        coords = [(r, c) for r in range(9) for c in range(9)]
        random.shuffle(coords)
        
        removed = 0
        for i in range(min(count, len(coords))):
            r, c = coords[i]
            if puzzle[r, c] != 0:
                puzzle[r, c] = 0
                removed += 1
            if removed >= count:
                break
        
        return puzzle
    
    @staticmethod
    def _fallback_generate(target_removal):
        """Fallback method to generate a basic puzzle."""
        print("Fallback: Generating a basic puzzle.")
        board = np.zeros((9, 9), dtype=int)
        bt = BacktrackingSolver()
        bt.solve(board, randomize=True)
        return SudokuGenerator._remove_cells(board, target_removal)
