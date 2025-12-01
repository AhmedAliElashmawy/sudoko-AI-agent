# 🧩 Sudoku AI Agent

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![PyQt6](https://img.shields.io/badge/PyQt6-6.0+-green.svg)](https://www.riverbankcomputing.com/software/pyqt/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

An intelligent Sudoku solver and generator powered by **Constraint Satisfaction Problem (CSP)** algorithms. This application combines **Arc Consistency (AC-3)** and **Backtracking Search** to efficiently solve Sudoku puzzles while providing an interactive GUI for both AI-powered solving and manual play.

## 🏗️ Project Structure

```
sudoko-AI-agent/
├── main.py                    # Application entry point
├── requirements.txt           # Project dependencies
├── README.md                  # Documentation
├── LICENSE                    # MIT License
│
├── src/
│   ├── logic/                 # AI & Algorithm Implementation
│   │   ├── csp.py            # CSP framework (Variables, Domains, Constraints)
│   │   ├── ac3.py            # Arc Consistency Algorithm #3
│   │   ├── backtracking.py   # Backtracking Search algorithm
│   │   ├── solver.py         # Main solver orchestrator
│   │   └── generator.py      # Puzzle generation with difficulty classification
│   │
│   └── gui/                   # User Interface
│       ├── main_window.py    # Main application window
│       ├── board_widget.py   # 9x9 Sudoku grid widget
│       └── controls.py       # Control buttons and sidebar
│
└── analysis/
    └── benchmark.py           # Performance testing and visualization

```

## 🧠 Algorithm Details

### Constraint Satisfaction Problem (CSP)

The Sudoku puzzle is modeled as a CSP with:

- **Variables**: 81 cells (9×9 grid), indexed 0-80
- **Domains**: Possible values {1-9} for each cell
- **Constraints**: Three types of constraints:
  - **Row Constraints**: No duplicates in any row
  - **Column Constraints**: No duplicates in any column
  - **Box Constraints**: No duplicates in any 3×3 sub-grid

### Arc Consistency (AC-3)

The AC-3 algorithm reduces the search space by:
1. Maintaining a queue of arcs (variable pairs with constraints)
2. Iteratively removing inconsistent values from domains
3. Propagating constraints until arc-consistency is achieved

**Benefits**: Often solves easy puzzles without backtracking

### Backtracking Search

When AC-3 alone cannot solve the puzzle:
1. Select an unassigned variable (cell)
2. Try assigning values from its domain
3. Recursively solve the remaining puzzle
4. Backtrack if a dead-end is reached

**Features**:
- Standard recursive solving
- Randomized solving for puzzle generation
- Efficient pruning of invalid states

### Hybrid Solver

The `solver.py` module combines both algorithms:
1. First applies AC-3 to reduce domains
2. If not fully solved, uses Backtracking on the reduced problem
3. Achieves optimal performance across all difficulty levels

## 📊 Difficulty Classification

Puzzles are classified based on the AI approach required, not just the number of clues:

| Difficulty | Solving Method | Description |
|-----------|----------------|-------------|
| **Easy** | AC-3 only | Solved purely by constraint propagation (0 guesses) |
| **Medium** | AC-3 + Shallow Backtracking | AC-3 reduces the problem significantly |
| **Hard** | AC-3 + Deep Backtracking | Requires extensive search and multiple guesses |

## 📈 Performance Benchmarking

Run the benchmark script to analyze solver performance:

```bash
python analysis/benchmark.py
```

This generates:
- Solving time vs. difficulty analysis
- Performance metrics for 50+ puzzles
- Visualization plots saved to `plots/` directory

## 🛠️ Technologies Used

- **Python 3.8+**: Core programming language
- **PyQt6**: Modern GUI framework
- **NumPy**: Efficient numerical operations
- **Matplotlib**: Data visualization and plotting

## 📝 File Descriptions

### Core Modules

- **`main.py`**: Application entry point, initializes PyQt6 and launches the GUI
- **`csp.py`**: Fundamental CSP classes (Variable, Domain, Constraint)
- **`ac3.py`**: Arc Consistency Algorithm implementation
- **`backtracking.py`**: Backtracking Search with randomization support
- **`solver.py`**: Orchestrates AC-3 and Backtracking for optimal solving
- **`generator.py`**: Creates new puzzles with difficulty classification

### GUI Components

- **`main_window.py`**: Main application container, manages mode switching
- **`board_widget.py`**: Renders the 9×9 grid, handles user input and visual feedback
- **`controls.py`**: Sidebar buttons and control panel

### Analysis Tools

- **`benchmark.py`**: Performance testing script with visualization

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.