import sys
import os
from PyQt6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QMessageBox
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QShortcut, QKeySequence
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
        self.board_states = []  # Store board states from AC-3
        self.current_step = 0  # Current step index for navigation
        self.setup_ui()
        self.setup_keyboard_shortcuts()
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
        self.controls_widget.next_step_clicked.connect(self.next_step)
        self.controls_widget.previous_step_clicked.connect(self.previous_step)
        main_layout.addWidget(self.controls_widget, stretch=1)
        
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)
        self.board_widget.enable_validation()
    
    def setup_keyboard_shortcuts(self):
        """Setup keyboard shortcuts for navigation."""
        # Left arrow or 'A' for previous step
        self.shortcut_prev = QShortcut(QKeySequence(Qt.Key.Key_Left), self)
        self.shortcut_prev.activated.connect(self.previous_step)
        
        self.shortcut_prev_a = QShortcut(QKeySequence('A'), self)
        self.shortcut_prev_a.activated.connect(self.previous_step)
        
        # Right arrow or 'D' for next step
        self.shortcut_next = QShortcut(QKeySequence(Qt.Key.Key_Right), self)
        self.shortcut_next.activated.connect(self.next_step)
        
        self.shortcut_next_d = QShortcut(QKeySequence('D'), self)
        self.shortcut_next_d.activated.connect(self.next_step)
    
    def generate_board(self):
        """Generate a new Sudoku puzzle."""
        # try:
        print(self.controls_widget.get_difficulty())
        puzzle = self.sudoku_generator.generate(self.controls_widget.get_difficulty())
        self.board_widget.set_board(puzzle, save_original=True)
        
        # Clear board states and hide step navigation
        self.board_states = []
        self.current_step = 0
        self.controls_widget.hide_step_navigation()
        self.controls_widget.hide_statistics()
        
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
            
            # Check for constraint violations in initial board
            if not self.is_valid_initial_board(puzzel):
                QMessageBox.warning(self, "Invalid Board", "Board has constraint violations. Check for duplicate numbers in rows, columns, or 3x3 boxes.")
                return

            # Check if board has at least 17 values (minimum for valid Sudoku)
            filled_count = np.count_nonzero(puzzel)
            if filled_count < 17:
                QMessageBox.warning(self, "Invalid Board", f"Board must have at least 17 filled cells to have a unique solution. Current: {filled_count}")
                return
            
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
        self.success, self.solution, self.method = solver.solve(log_steps=True, log_file="ac3_solve_log.txt")
        
        # Store board states from AC-3 for GUI display
        self.board_states = solver.get_board_states()
        self.current_step = 0
        print(f"\n>>> Captured {len(self.board_states)} board states for GUI display")
        print(f">>> Solve time: {solver.solve_time:.4f} seconds")
        
        if self.success:
            # Show the first step (initial state)
            if len(self.board_states) > 0:
                self.board_widget.set_board(self.board_states[0], save_original=False)
                self.controls_widget.update_step_info(0, len(self.board_states))
            else:
                self.board_widget.set_board(self.solution, save_original=False)
            
            # Update statistics display
            self.controls_widget.update_statistics(
                solver.solve_time,
                self.method,
                len(self.board_states)
            )
        else:
            QMessageBox.warning(self, "No Solution", "The AI couldn't find a solution for this puzzle.")
                
        # except Exception as e:
            # QMessageBox.critical(self, "Error", f"Failed to solve puzzle: {str(e)}")
    
    def reset_board(self):
        """Reset the board to the original puzzle."""
        self.board_widget.reset_to_original()
        # Reset to first step if states are available
        if self.board_states:
            self.current_step = 0
            self.board_widget.set_board(self.board_states[0], save_original=False)
            self.controls_widget.update_step_info(0, len(self.board_states))

    def clear_board(self):
        self.board_widget.clear_board()
        # Clear board states and hide step navigation
        self.board_states = []
        self.current_step = 0
        self.controls_widget.hide_step_navigation()
        self.controls_widget.hide_statistics()
    
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
    
    def is_valid_initial_board(self, board):
        """Check if initial board state has no constraint violations."""
        # Check rows
        for row in range(9):
            row_values = board[row, :][board[row, :] != 0]
            if len(row_values) != len(set(row_values)):
                return False
        
        # Check columns
        for col in range(9):
            col_values = board[:, col][board[:, col] != 0]
            if len(col_values) != len(set(col_values)):
                return False
        
        # Check 3x3 boxes
        for box_row in range(0, 9, 3):
            for box_col in range(0, 9, 3):
                box = board[box_row:box_row+3, box_col:box_col+3].flatten()
                box_values = box[box != 0]
                if len(box_values) != len(set(box_values)):
                    return False
        
        return True
    
    def on_mode_changed(self, mode):
        """Handle mode changes."""
        if mode == "Player" or mode == "Custom Board":
            self.board_widget.set_editable(True)
            # Enable validation only in Player mode
            self.board_widget.enable_validation(mode == "Player")
        else:
            self.board_widget.set_editable(False)
            self.board_widget.enable_validation(False)
    
    def on_difficulty_changed(self, difficulty):
        """Handle difficulty changes."""
        self.current_difficulty = difficulty
    
    def get_board_states(self):
        """
        Returns the list of board states captured during AC-3 execution.
        Can be used to visualize the solving process step by step.
        """
        return self.board_states
    
    def next_step(self):
        """Navigate to the next AC-3 step."""
        if self.board_states and self.current_step < len(self.board_states) - 1:
            self.current_step += 1
            self.board_widget.set_board(self.board_states[self.current_step], save_original=False)
            self.controls_widget.update_step_info(self.current_step, len(self.board_states))
    
    def previous_step(self):
        """Navigate to the previous AC-3 step."""
        if self.board_states and self.current_step > 0:
            self.current_step -= 1
            self.board_widget.set_board(self.board_states[self.current_step], save_original=False)
            self.controls_widget.update_step_info(self.current_step, len(self.board_states))
