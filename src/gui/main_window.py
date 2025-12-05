import sys
import os
from PyQt6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QMessageBox
from PyQt6.QtCore import Qt
import numpy as np


sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'logic'))
from generator import SudokuGenerator
from solver import SudokuSolver
from backtracking import Backtracking

from board_widget import BoardWidget
from controls import ControlsWidget


class SudokuMainWindow(QMainWindow):
    """Main application window for Sudoku game."""
    
    def __init__(self):
        super().__init__()
        self.sudoku_generator = SudokuGenerator()
        self.solution = None
        self.success = False
        self.method = ""
        self.setup_ui()
        self.setWindowTitle("Sudoku Game - AI & Player Mode")
        self.resize(900, 650)
    
    def setup_ui(self):
        """Create the main window layout."""
        central_widget = QWidget()
        main_layout = QHBoxLayout()
        
        # Board widget (left side)
        self.board_widget = BoardWidget()
        main_layout.addWidget(self.board_widget, stretch=2)
        
        # Controls widget (right side)
        self.controls_widget = ControlsWidget()
        self.controls_widget.generate_clicked.connect(self.generate_board)
        self.controls_widget.solve_clicked.connect(self.solve_board)
        self.controls_widget.reset_clicked.connect(self.reset_board)
        self.controls_widget.check_clicked.connect(self.check_solution)
        self.controls_widget.clear_clicked.connect(self.clear_board)
        self.controls_widget.mode_changed.connect(self.on_mode_changed)
        self.controls_widget.difficulty_changed.connect(self.on_difficulty_changed)
        main_layout.addWidget(self.controls_widget, stretch=1)
        
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)
    
    def generate_board(self):
        """Generate a new Sudoku puzzle."""
        # try:
        puzzle = self.sudoku_generator.generate(self.controls_widget.get_difficulty())
        self.board_widget.set_board(puzzle, save_original=True)
        
        # Solve it to store the solution
        # if success:
        #     self.success = success
        #     self.solution = board_solution
        #     self.method = method
        # else:
        #     self.solution = None
        
        # Set editability based on mode
        if self.controls_widget.get_mode() == "Player":
            self.board_widget.set_editable(True)
        else:
            self.board_widget.set_editable(False)
                
        # except Exception as e:
        #     QMessageBox.critical(self, "Error", f"Failed to generate puzzle: {str(e)}")
    
    def solve_board(self):
        """Solve the current puzzle."""
        # try:
        puzzel = self.board_widget.get_board()
        if self.controls_widget.get_mode() == "Custom Board":
            print("custom")
            bt = Backtracking()
            # Check solvability
            test_board = puzzel.copy()
            solvability = bt.btGenerate(test_board, False)
            if solvability:
                # Check uniqueness
                test_board2 = puzzel.copy()
                solutions = bt.countSolutions(test_board2, 2)
                if solutions > 1:
                    QMessageBox.information(self, "Solvability Check", "This puzzle has multiple solutions (not unique), Arc Consistency cant solve ununique puzzels.")
                    return
                else:
                    QMessageBox.information(self, "Solvability Check", "This puzzle has a unique solution!")
            else:
                QMessageBox.warning(self, "Solvability Check", "This puzzle is not solvable.")
                return
        solver = SudokuSolver(puzzel)
        self.success, self.solution, self.method = solver.solve()
        if self.success:
            self.board_widget.set_board(self.solution, save_original=False)
            QMessageBox.information(self, "Success", f"The AI has solved the puzzle!\nMethod: {self.method}")
        else:
            QMessageBox.warning(self, "No Solution", "The AI couldn't find a solution for this puzzle.")
                
        # except Exception as e:
            # QMessageBox.critical(self, "Error", f"Failed to solve puzzle: {str(e)}")
    
    def reset_board(self):
        """Reset the board to the original puzzle."""
        self.board_widget.reset_to_original()

    def clear_board(self):
        self.board_widget.clear_board()
    
    def check_solution(self):
        """Check if the player's solution is correct."""
        try:
            # Check if board is complete
            if not self.board_widget.is_complete():
                QMessageBox.information(self, "Incomplete", "Please fill in all cells before checking.")
                return
            
            current_board = self.board_widget.get_board()
            
            # Validate the solution
            if self.is_valid_solution(current_board):
                QMessageBox.information(self, "Congratulations!", "🎉 Your solution is correct! Well done!")
            else:
                QMessageBox.warning(self, "Incorrect", "Your solution has errors. Keep trying!")
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to check solution: {str(e)}")
    
    def is_valid_solution(self, board):
        """Validate if the board satisfies all Sudoku constraints."""
        # This will be changed to check using the already solved board
        # Check rows
        for row in range(9):
            if not self.is_valid_group(board[row, :]):
                return False
        
        # Check columns
        for col in range(9):
            if not self.is_valid_group(board[:, col]):
                return False
        
        # Check 3x3 boxes
        for box_row in range(0, 9, 3):
            for box_col in range(0, 9, 3):
                box = board[box_row:box_row+3, box_col:box_col+3].flatten()
                if not self.is_valid_group(box):
                    return False
        
        return True
    
    def is_valid_group(self, group):
        """Check if a group (row/column/box) has all digits 1-9 without repetition."""
        group = group[group != 0]  # Remove zeros
        return len(group) == 9 and len(set(group)) == 9 and all(1 <= x <= 9 for x in group)
    
    def on_mode_changed(self, mode):
        """Handle mode changes."""
        if mode == "Player" or mode == "Custom Board":
            self.board_widget.set_editable(True)
        else:
            self.board_widget.set_editable(False)
    
    def on_difficulty_changed(self, difficulty):
        """Handle difficulty changes."""
        self.current_difficulty = difficulty
