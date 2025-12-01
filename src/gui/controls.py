from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                              QLabel, QComboBox, QGroupBox, QMessageBox)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont


class ControlsWidget(QWidget):
    """Widget containing all game controls and mode selection."""
    
    generate_clicked = pyqtSignal()
    solve_clicked = pyqtSignal()
    reset_clicked = pyqtSignal()
    check_clicked = pyqtSignal()
    mode_changed = pyqtSignal(str)
    difficulty_changed = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.current_mode = "Player"
        self.setup_ui()
    
    def setup_ui(self):
        """Create the control panel layout."""
        main_layout = QVBoxLayout()
        
        # Title
        title = QLabel("Sudoku Game")
        title.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title)
        
        # Mode selection
        mode_group = QGroupBox()
        mode_layout = QVBoxLayout()
        
        mode_label = QLabel("Select Mode:")
        mode_label.setFont(QFont("Arial", 12))
        mode_layout.addWidget(mode_label)
        
        self.mode_combo = QComboBox()
        self.mode_combo.addItems(["Player", "AI Solver"])
        self.mode_combo.setFont(QFont("Arial", 11))
        self.mode_combo.currentTextChanged.connect(self.on_mode_changed)
        mode_layout.addWidget(self.mode_combo)
        
        mode_group.setLayout(mode_layout)
        main_layout.addWidget(mode_group)
        
        # Difficulity selection
        difficulty_group = QGroupBox()
        difficulty_layout = QVBoxLayout()
        
        difficulty_label = QLabel("Select Difficulty:")
        difficulty_label.setFont(QFont("Arial", 12))
        difficulty_layout.addWidget(difficulty_label)
        
        self.difficulty_combo = QComboBox()
        self.difficulty_combo.addItems(["Easy", "Medium", "Hard"])
        self.difficulty_combo.setFont(QFont("Arial", 11))
        self.difficulty_combo.currentTextChanged.connect(self.difficulty_changed.emit)
        difficulty_layout.addWidget(self.difficulty_combo)
        
        difficulty_group.setLayout(difficulty_layout)
        main_layout.addWidget(difficulty_group)

        # Action buttons
        buttons_group = QGroupBox()
        buttons_layout = QVBoxLayout()
        actions_label = QLabel("Actions:")
        actions_label.setFont(QFont("Arial", 12))
        buttons_layout.addWidget(actions_label)
        
        # Generate button
        self.generate_btn = QPushButton("Generate New Board")
        self.generate_btn.setFont(QFont("Arial", 11))
        self.generate_btn.setMinimumHeight(40)
        self.generate_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
        """)
        self.generate_btn.clicked.connect(self.generate_clicked.emit)
        buttons_layout.addWidget(self.generate_btn)
        
        # Solve button (AI mode)
        self.solve_btn = QPushButton("Solve with AI")
        self.solve_btn.setFont(QFont("Arial", 11))
        self.solve_btn.setMinimumHeight(40)
        self.solve_btn.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #0b7dda;
            }
            QPushButton:pressed {
                background-color: #0a6bc2;
            }
            QPushButton:disabled {
                background-color: #cccccc;
                color: #666666;
            }
        """)
        self.solve_btn.clicked.connect(self.solve_clicked.emit)
        self.solve_btn.setVisible(False)  # Hidden in Player mode
        buttons_layout.addWidget(self.solve_btn)
        
        # Check solution button (Player mode)
        self.check_btn = QPushButton("Check Solution")
        self.check_btn.setFont(QFont("Arial", 11))
        self.check_btn.setMinimumHeight(40)
        self.check_btn.setStyleSheet("""
            QPushButton {
                background-color: #FF9800;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #e68900;
            }
            QPushButton:pressed {
                background-color: #cc7a00;
            }
        """)
        self.check_btn.clicked.connect(self.check_clicked.emit)
        buttons_layout.addWidget(self.check_btn)
        
        # Reset button
        self.reset_btn = QPushButton("Reset Board")
        self.reset_btn.setFont(QFont("Arial", 11))
        self.reset_btn.setMinimumHeight(40)
        self.reset_btn.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #da190b;
            }
            QPushButton:pressed {
                background-color: #c41609;
            }
        """)
        self.reset_btn.clicked.connect(self.reset_clicked.emit)
        buttons_layout.addWidget(self.reset_btn)
        
        buttons_group.setLayout(buttons_layout)
        main_layout.addWidget(buttons_group)
        
        main_layout.addStretch()
        self.setLayout(main_layout)
    
    def on_mode_changed(self, mode):
        """Handle mode change between Player and AI."""
        self.current_mode = mode
        
        if mode == "AI Solver":
            self.solve_btn.setVisible(True)
            self.check_btn.setVisible(False)
        else:
            self.solve_btn.setVisible(False)
            self.check_btn.setVisible(True)
        
        self.mode_changed.emit(mode)
    
    def get_mode(self):
        """Return the current mode."""
        return self.current_mode
    
    def get_difficulty(self):
        """Return the current difficulty level."""
        return self.difficulty_combo.currentText()
