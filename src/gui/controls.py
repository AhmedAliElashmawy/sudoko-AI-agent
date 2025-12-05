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
    clear_clicked = pyqtSignal()
    mode_changed = pyqtSignal(str)
    difficulty_changed = pyqtSignal(str)
    next_step_clicked = pyqtSignal()
    previous_step_clicked = pyqtSignal()
    
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
        self.mode_combo.addItems(["Player", "AI Solver", "Custom Board"])
        self.mode_combo.setFont(QFont("Arial", 11))
        self.mode_combo.currentTextChanged.connect(self.on_mode_changed)
        mode_layout.addWidget(self.mode_combo)
        
        mode_group.setLayout(mode_layout)
        main_layout.addWidget(mode_group)
        
        # Difficulity selection
        self.difficulty_group = QGroupBox()
        self.difficulty_layout = QVBoxLayout()
        
        difficulty_label = QLabel("Select Difficulty:")
        difficulty_label.setFont(QFont("Arial", 12))
        self.difficulty_layout.addWidget(difficulty_label)
        
        self.difficulty_combo = QComboBox()
        self.difficulty_combo.addItems(["Easy", "Medium", "Hard"])
        self.difficulty_combo.setFont(QFont("Arial", 11))
        self.difficulty_combo.currentTextChanged.connect(self.difficulty_changed.emit)
        self.difficulty_layout.addWidget(self.difficulty_combo)
        
        self.difficulty_group.setLayout(self.difficulty_layout)
        main_layout.addWidget(self.difficulty_group)

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

        self.clear_btn = QPushButton("Clear Board")
        self.clear_btn.setFont(QFont("Arial", 11))
        self.clear_btn.setMinimumHeight(40)
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
        self.clear_btn.clicked.connect(self.clear_clicked.emit)
        buttons_layout.addWidget(self.clear_btn)

        buttons_group.setLayout(buttons_layout)
        main_layout.addWidget(buttons_group)
        
        # Step navigation group (for AC3 visualization)
        self.step_group = QGroupBox()
        step_layout = QVBoxLayout()
        
        step_label = QLabel("AC3 Step Navigation:")
        step_label.setFont(QFont("Arial", 12))
        step_layout.addWidget(step_label)
        
        self.step_info_label = QLabel("No steps available")
        self.step_info_label.setFont(QFont("Arial", 10))
        self.step_info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        step_layout.addWidget(self.step_info_label)
        
        # Navigation buttons in horizontal layout
        nav_layout = QHBoxLayout()
        
        self.prev_step_btn = QPushButton("◀ Previous")
        self.prev_step_btn.setFont(QFont("Arial", 10))
        self.prev_step_btn.setMinimumHeight(35)
        self.prev_step_btn.setEnabled(False)
        self.prev_step_btn.setStyleSheet("""
            QPushButton {
                background-color: #607D8B;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px;
            }
            QPushButton:hover:enabled {
                background-color: #546E7A;
            }
            QPushButton:pressed {
                background-color: #455A64;
            }
            QPushButton:disabled {
                background-color: #cccccc;
                color: #666666;
            }
        """)
        self.prev_step_btn.clicked.connect(self.previous_step_clicked.emit)
        nav_layout.addWidget(self.prev_step_btn)
        
        self.next_step_btn = QPushButton("Next ▶")
        self.next_step_btn.setFont(QFont("Arial", 10))
        self.next_step_btn.setMinimumHeight(35)
        self.next_step_btn.setEnabled(False)
        self.next_step_btn.setStyleSheet("""
            QPushButton {
                background-color: #607D8B;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px;
            }
            QPushButton:hover:enabled {
                background-color: #546E7A;
            }
            QPushButton:pressed {
                background-color: #455A64;
            }
            QPushButton:disabled {
                background-color: #cccccc;
                color: #666666;
            }
        """)
        self.next_step_btn.clicked.connect(self.next_step_clicked.emit)
        nav_layout.addWidget(self.next_step_btn)
        
        step_layout.addLayout(nav_layout)
        self.step_group.setLayout(step_layout)
        self.step_group.setVisible(False)  # Hidden by default
        main_layout.addWidget(self.step_group)
        
        # Solve statistics group
        self.stats_group = QGroupBox()
        stats_layout = QVBoxLayout()
        
        stats_label = QLabel("Solve Statistics:")
        stats_label.setFont(QFont("Arial", 12))
        stats_layout.addWidget(stats_label)
        
        self.time_label = QLabel("Time: N/A")
        self.time_label.setFont(QFont("Arial", 10))
        self.time_label.setStyleSheet("color: #2196F3; font-weight: bold;")
        stats_layout.addWidget(self.time_label)
        
        self.method_label = QLabel("Method: N/A")
        self.method_label.setFont(QFont("Arial", 10))
        self.method_label.setStyleSheet("color: #4CAF50; font-weight: bold;")
        stats_layout.addWidget(self.method_label)
        
        self.steps_label = QLabel("Steps: N/A")
        self.steps_label.setFont(QFont("Arial", 10))
        self.steps_label.setStyleSheet("color: #FF9800; font-weight: bold;")
        stats_layout.addWidget(self.steps_label)
        
        self.stats_group.setLayout(stats_layout)
        self.stats_group.setVisible(False)  # Hidden by default
        main_layout.addWidget(self.stats_group)
        
        main_layout.addStretch()
        self.setLayout(main_layout)
    
    def on_mode_changed(self, mode):
        """Handle mode change between Player and AI."""
        self.current_mode = mode
        
        if mode == "AI Solver":
            self.solve_btn.setVisible(True)
            self.check_btn.setVisible(False)
            self.difficulty_group.setVisible(True)
            self.generate_btn.setVisible(True)
        elif mode == "Custom Board":
            self.solve_btn.setVisible(True)
            self.check_btn.setVisible(False)
            self.difficulty_group.setVisible(False)
            self.generate_btn.setVisible(False)
        else:
            self.solve_btn.setVisible(False)
            self.check_btn.setVisible(True)
            self.difficulty_group.setVisible(True)
            self.generate_btn.setVisible(True)
        self.mode_changed.emit(mode)
    
    def get_mode(self):
        """Return the current mode."""
        return self.current_mode
    
    def get_difficulty(self):
        """Return the current difficulty level."""
    
    def update_step_info(self, current_step, total_steps):
        """Update the step information label."""
        if total_steps > 0:
            self.step_info_label.setText(f"Step {current_step + 1} / {total_steps}")
            self.step_group.setVisible(True)
            self.prev_step_btn.setEnabled(current_step > 0)
            self.next_step_btn.setEnabled(current_step < total_steps - 1)
        else:
            self.step_info_label.setText("No steps available")
            self.step_group.setVisible(False)
    
    def hide_step_navigation(self):
        """Hide the step navigation group."""
        self.step_group.setVisible(False)
    
    def update_statistics(self, solve_time, method, num_steps):
        """Update the solve statistics display."""
        self.time_label.setText(f"Time: {solve_time:.4f} seconds")
        self.method_label.setText(f"Method: {method}")
        self.steps_label.setText(f"Steps: {num_steps}")
        self.stats_group.setVisible(True)
    
    def hide_statistics(self):
        """Hide the statistics group."""
        self.stats_group.setVisible(False)
        return self.difficulty_combo.currentText()
