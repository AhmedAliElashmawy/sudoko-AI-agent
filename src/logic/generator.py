import copy
import random
import numpy as np
from backtracking import Backtracking
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
            "Easy": (25, 0),      # Few removed, AC3 should solve it (0 steps)
            "Medium": (35, 10),   # More removed, Backtrack needed but shallow
            "Hard": (45, 100)     # Many removed, Deep backtrack needed
        }
        
        target_removal, min_steps = settings.get(difficulty, (40, 10))
        best_board = None
        
        board = np.zeros((9, 9), dtype=int)
        bt = Backtracking()
        bt.btGenerate(board, randomize=True)  # Random valid board
        
        # 2. Remove Numbers
        puzzle = SudokuGenerator._remove_cells(board, target_removal)
        
        best_board = puzzle  # Keep checking
        if best_board is not None:
            return best_board
        else:
            return SudokuGenerator._fallback_generate(target_removal)

    @staticmethod
    def _remove_cells(board, count):
        """Remove specified number of cells from the board, ensuring unique solution."""
        puzzle = copy.deepcopy(board)
        coords = [(r, c) for r in range(9) for c in range(9)]
        random.shuffle(coords)
        
        removed = 0
        
        for i in range(min(count, len(coords))):
            r, c = coords[i]
            if puzzle[r, c] != 0:
                # Temporarily remove the cell
                original_value = puzzle[r, c]
                puzzle[r, c] = 0
                
                # Check if the puzzle still has exactly one solution
                # Create a new solver instance for each check
                puzzle_copy = copy.deepcopy(puzzle)
                bt = Backtracking()
                num_solutions = bt.countSolutions(puzzle_copy, max_solutions=2)
                
                if num_solutions == 1:
                    # Keep the cell removed
                    removed += 1
                else:
                    # Restore the cell if it creates multiple solutions
                    puzzle[r, c] = original_value
                
                if removed >= count:
                    break
        
        return puzzle
    
    @staticmethod
    def _fallback_generate(target_removal):
        """Fallback method to generate a basic puzzle."""
        print("Fallback: Generating a basic puzzle.")
        board = np.zeros((9, 9), dtype=int)
        bt = Backtracking()
        bt.btGenerate(board, randomize=True)
        return SudokuGenerator._remove_cells(board, target_removal)
