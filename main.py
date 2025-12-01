import sys
import os
from PyQt6.QtWidgets import QApplication

# Add the gui directory to path dynamically
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src', 'gui'))
from main_window import SudokuMainWindow


def main():
    """Main entry point for the Sudoku application."""
    app = QApplication(sys.argv)
    
    # Set application style
    app.setStyle('Fusion')
    
    # Create and show main window
    window = SudokuMainWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
