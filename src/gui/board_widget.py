from PyQt6.QtWidgets import QWidget, QGridLayout, QLineEdit
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QPalette, QColor
import numpy as np


class SudokuCell(QLineEdit):
    """Custom QLineEdit for a single Sudoku cell."""
    
    def __init__(self, row, col, is_given=False):
        super().__init__()
        self.row = row
        self.col = col
        self.is_given = is_given
        self.setup_ui()
    
    def setup_ui(self):
        """Configure cell appearance and behavior."""
        self.setMaxLength(1)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        font = QFont("Arial", 20, QFont.Weight.Bold)
        self.setFont(font)
        
        self.setFixedSize(65, 65)
        
        # Determine border styles based on position
        top_border = "2px solid #000" if self.row % 3 == 0 else "1px solid #999"
        left_border = "2px solid #000" if self.col % 3 == 0 else "1px solid #999"
        bottom_border = "2px solid #000" if self.row == 8 or (self.row + 1) % 3 == 0 else "1px solid #999"
        right_border = "2px solid #000" if self.col == 8 or (self.col + 1) % 3 == 0 else "1px solid #999"
        
        if self.is_given:
            self.setReadOnly(True)
            self.setStyleSheet(f"""
                QLineEdit {{
                    background-color: white;
                    color: #000000;
                    border-top: {top_border};
                    border-left: {left_border};
                    border-bottom: {bottom_border};
                    border-right: {right_border};
                    font-weight: bold;
                }}
            """)
        else:
            self.setStyleSheet(f"""
                QLineEdit {{
                    background-color: white;
                    color: #0066cc;
                    border-top: {top_border};
                    border-left: {left_border};
                    border-bottom: {bottom_border};
                    border-right: {right_border};
                }}
                QLineEdit:focus {{
                    background-color: #e3f2fd;
                }}
            """)
    
    def set_value(self, value, is_given=False):
        """Set the cell value and update its appearance."""
        if value == 0:
            self.setText("")
        else:
            self.setText(str(value))
        
        self.is_given = is_given
        self.setup_ui()
    
    def highlight_error(self, is_error=True):
        """Highlight the cell in red if it contains an error."""
        top_border = "2px solid #000" if self.row % 3 == 0 else "1px solid #999"
        left_border = "2px solid #000" if self.col % 3 == 0 else "1px solid #999"
        bottom_border = "2px solid #000" if self.row == 8 or (self.row + 1) % 3 == 0 else "1px solid #999"
        right_border = "2px solid #000" if self.col == 8 or (self.col + 1) % 3 == 0 else "1px solid #999"
        
        if self.is_given:
            # Given cells don't change
            return
        
        if is_error:
            self.setStyleSheet(f"""
                QLineEdit {{
                    background-color: #ffcccc;
                    color: #cc0000;
                    border-top: {top_border};
                    border-left: {left_border};
                    border-bottom: {bottom_border};
                    border-right: {right_border};
                    font-weight: bold;
                }}
                QLineEdit:focus {{
                    background-color: #ffb3b3;
                }}
            """)
        else:
            self.setStyleSheet(f"""
                QLineEdit {{
                    background-color: white;
                    color: #0066cc;
                    border-top: {top_border};
                    border-left: {left_border};
                    border-bottom: {bottom_border};
                    border-right: {right_border};
                }}
                QLineEdit:focus {{
                    background-color: #e3f2fd;
                }}
            """)
    
    def get_value(self):
        """Get the numeric value of the cell."""
        text = self.text().strip()
        if text.isdigit() and 1 <= int(text) <= 9:
            return int(text)
        return 0


class BoardWidget(QWidget):
    """Widget displaying the 9x9 Sudoku board."""
    
    board_changed = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.cells = {}
        self.original_board = None
        self.validation_enabled = False
        self.setup_ui()
    
    def setup_ui(self):
        """Create the grid layout with cells."""
        layout = QGridLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        
        for row in range(9):
            for col in range(9):
                cell = SudokuCell(row, col)
                cell.textChanged.connect(self.on_cell_changed)
                self.cells[(row, col)] = cell
                layout.addWidget(cell, row, col)
        
        self.setLayout(layout)
        
        # Add a border around the entire board
        self.setStyleSheet("""
            BoardWidget {
                border: 3px solid #000;
            }
        """)
    
    def on_cell_changed(self):
        """Emit signal when any cell changes."""
        if self.validation_enabled:
            self.validate_all_cells()
        self.board_changed.emit()
    
    def set_board(self, board, save_original=True):
        """Load a board into the widget."""
        if save_original:
            self.original_board = board.copy()
        
        for row in range(9):
            for col in range(9):
                value = int(board[row, col])
                is_given = (value != 0) if save_original else False
                self.cells[(row, col)].set_value(value, is_given)
    
    def get_board(self):
        """Get the current board state as a numpy array."""
        board = np.zeros((9, 9), dtype=int)
        for row in range(9):
            for col in range(9):
                board[row, col] = self.cells[(row, col)].get_value()
        return board
    
    def reset_to_original(self):
        """Reset the board to the original puzzle."""
        if self.original_board is not None:
            self.set_board(self.original_board, save_original=False)
    
    def clear_board(self):
        """Clear all cells."""
        empty_board = np.zeros((9, 9), dtype=int)
        self.set_board(empty_board, save_original=True)
    
    def set_editable(self, editable):
        """Enable or disable editing of non-given cells."""
        for cell in self.cells.values():
            # if not cell.is_given:
            cell.setReadOnly(not editable)
    
    def is_complete(self):
        """Check if all cells are filled."""
        for cell in self.cells.values():
            if cell.get_value() == 0:
                return False
        return True
    
    def enable_validation(self, enabled=True):
        """Enable or disable real-time validation."""
        self.validation_enabled = enabled
        if enabled:
            self.validate_all_cells()
        else:
            # Reset all cell colors
            for cell in self.cells.values():
                if not cell.is_given:
                    cell.highlight_error(False)
    
    def validate_all_cells(self):
        """Validate all cells and highlight errors."""
        board = self.get_board()
        
        for (row, col), cell in self.cells.items():
            if cell.is_given:
                continue
            
            value = cell.get_value()
            if value == 0:
                cell.highlight_error(False)
                continue
            
            # Check if this value violates constraints
            has_error = self.check_cell_conflict(board, row, col, value)
            cell.highlight_error(has_error)
    
    def check_cell_conflict(self, board, row, col, value):
        """Check if placing value at (row, col) creates a conflict."""
        # Check row (excluding the cell itself)
        for c in range(9):
            if c != col and board[row, c] == value:
                return True
        
        # Check column (excluding the cell itself)
        for r in range(9):
            if r != row and board[r, col] == value:
                return True
        
        # Check 3x3 box (excluding the cell itself)
        box_row, box_col = (row // 3) * 3, (col // 3) * 3
        for r in range(box_row, box_row + 3):
            for c in range(box_col, box_col + 3):
                if (r, c) != (row, col) and board[r, c] == value:
                    return True
        
        return False
