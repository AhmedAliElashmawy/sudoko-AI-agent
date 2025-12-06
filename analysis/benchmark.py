"""
Benchmark Analysis for Sudoku Solver
Compares AC3 performance across different difficulty levels.
Note: Backtracking is used only for puzzle generation and validation, not for solving.
"""

import sys
import os
import numpy as np
import time
import matplotlib.pyplot as plt
from collections import defaultdict

# Add parent directory to path to import modules
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src', 'logic'))

from generator import SudokuGenerator
from solver import SudokuSolver
from csp import CSP


class SudokuBenchmark:
    """
    Benchmark suite for comparing AC3 solver performance
    across different difficulty levels.
    Measures time and arc revisions (domain reductions) during AC3 execution.
    """
    
    def __init__(self, num_puzzles_per_difficulty=10):
        """
        Initialize benchmark suite.
        
        Args:
            num_puzzles_per_difficulty: Number of puzzles to test per difficulty level
        """
        self.num_puzzles = num_puzzles_per_difficulty
        self.results = defaultdict(list)
        self.difficulties = ["Easy", "Medium", "Hard"]
        
    def run_benchmark(self):
        """
        Run comprehensive benchmark across all difficulty levels.
        Measures time and domain reductions for AC3 solving.
        """
        print("=" * 60)
        print("SUDOKU AC3 SOLVER BENCHMARK")
        print("=" * 60)
        print(f"Testing {self.num_puzzles} puzzles per difficulty level")
        print("Note: Backtracking is used only for generation, not solving\n")
        
        for difficulty in self.difficulties:
            print(f"\n{'=' * 60}")
            print(f"Testing {difficulty} puzzles...")
            print('=' * 60)
            
            for i in range(self.num_puzzles):
                print(f"\n[{difficulty}] Puzzle {i+1}/{self.num_puzzles}")
                
                # Generate puzzle (uses backtracking for generation)
                puzzle = SudokuGenerator.generate(difficulty=difficulty)
                clues = np.count_nonzero(puzzle)
                empty_cells = 81 - clues
                print(f"  Clues: {clues}/81 (Empty cells: {empty_cells})")
                
                # Create CSP to count initial domain size
                csp_initial = CSP(puzzle)
                initial_domain_size = sum(len(csp_initial.domains[var]) for var in csp_initial.variables)
                
                # Solve with AC3 only
                solver = SudokuSolver(puzzle)
                start_time = time.time()
                success, solved_board, method = solver.solve(puzzle)
                elapsed_time = time.time() - start_time
                
                # Count final domain size and reductions
                csp_final = CSP(solved_board if success else puzzle)
                final_domain_size = sum(len(csp_final.domains[var]) for var in csp_final.variables)
                domain_reductions = initial_domain_size - final_domain_size
                
                # Count cells solved by AC3
                cells_solved = 0
                if success:
                    for r in range(9):
                        for c in range(9):
                            if puzzle[r, c] == 0 and solved_board[r, c] != 0:
                                cells_solved += 1
                
                self.results[difficulty].append({
                    'time': elapsed_time,
                    'domain_reductions': domain_reductions,
                    'cells_solved': cells_solved,
                    'method': method,
                    'clues': clues,
                    'empty_cells': empty_cells,
                    'success': success
                })
                
                print(f"  Method: {method}")
                print(f"  Cells Solved: {cells_solved}/{empty_cells}")
                print(f"  Domain Reductions: {domain_reductions}")
                print(f"  Time: {elapsed_time:.4f}s")
                print(f"  Success: {success}")
        
        print("\n" + "=" * 60)
        print("BENCHMARK COMPLETE")
        print("=" * 60)
        
    def print_statistics(self):
        """Print statistical summary of benchmark results."""
        print("\n" + "=" * 60)
        print("BENCHMARK STATISTICS")
        print("=" * 60)
        
        for difficulty in self.difficulties:
            if not self.results[difficulty]:
                continue
                
            times = [r['time'] for r in self.results[difficulty]]
            domain_reductions = [r['domain_reductions'] for r in self.results[difficulty]]
            cells_solved = [r['cells_solved'] for r in self.results[difficulty]]
            clues = [r['clues'] for r in self.results[difficulty]]
            success_rate = sum(1 for r in self.results[difficulty] if r['success']) / len(self.results[difficulty]) * 100
            
            print(f"\n{difficulty} Difficulty:")
            print(f"  Average Clues: {np.mean(clues):.1f}")
            print(f"  Average Time: {np.mean(times):.4f}s (±{np.std(times):.4f}s)")
            print(f"  Min Time: {np.min(times):.4f}s")
            print(f"  Max Time: {np.max(times):.4f}s")
            print(f"  Average Domain Reductions: {np.mean(domain_reductions):.1f} (±{np.std(domain_reductions):.1f})")
            print(f"  Average Cells Solved: {np.mean(cells_solved):.1f} (±{np.std(cells_solved):.1f})")
            print(f"  Success Rate: {success_rate:.1f}%")
    
    def plot_results(self):
        """Generate comparison plots for time and domain reductions across difficulty levels."""
        if not any(self.results.values()):
            print("No results to plot!")
            return
        
        # Prepare data for plotting
        difficulties = []
        avg_times = []
        std_times = []
        avg_reductions = []
        std_reductions = []
        avg_cells_solved = []
        std_cells_solved = []
        
        for difficulty in self.difficulties:
            if not self.results[difficulty]:
                continue
                
            difficulties.append(difficulty)
            times = [r['time'] for r in self.results[difficulty]]
            reductions = [r['domain_reductions'] for r in self.results[difficulty]]
            cells = [r['cells_solved'] for r in self.results[difficulty]]
            
            avg_times.append(np.mean(times))
            std_times.append(np.std(times))
            avg_reductions.append(np.mean(reductions))
            std_reductions.append(np.std(reductions))
            avg_cells_solved.append(np.mean(cells))
            std_cells_solved.append(np.std(cells))
        
        # Create figure with subplots
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        fig.suptitle('AC3 Solver Performance Benchmark', fontsize=16, fontweight='bold')
        
        # Plot 1: Average Time Comparison
        ax1 = axes[0, 0]
        bars1 = ax1.bar(difficulties, avg_times, yerr=std_times, 
                        capsize=5, alpha=0.7, color=['green', 'orange', 'red'])
        ax1.set_ylabel('Time (seconds)', fontsize=11)
        ax1.set_title('Average Solving Time by Difficulty', fontsize=12, fontweight='bold')
        ax1.grid(axis='y', alpha=0.3)
        
        # Add value labels on bars
        for bar, val in zip(bars1, avg_times):
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height,
                    f'{val:.4f}s', ha='center', va='bottom', fontsize=9)
        
        # Plot 2: Average Domain Reductions Comparison
        ax2 = axes[0, 1]
        bars2 = ax2.bar(difficulties, avg_reductions, yerr=std_reductions,
                        capsize=5, alpha=0.7, color=['green', 'orange', 'red'])
        ax2.set_ylabel('Domain Reductions', fontsize=11)
        ax2.set_title('Average Domain Reductions by Difficulty', fontsize=12, fontweight='bold')
        ax2.grid(axis='y', alpha=0.3)
        
        # Add value labels on bars
        for bar, val in zip(bars2, avg_reductions):
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height,
                    f'{val:.0f}', ha='center', va='bottom', fontsize=9)
        
        # Plot 3: Box plot for Time Distribution
        ax3 = axes[1, 0]
        time_data = [np.array([r['time'] for r in self.results[d]]) 
                     for d in self.difficulties if self.results[d]]
        bp1 = ax3.boxplot(time_data, labels=difficulties, patch_artist=True)
        
        # Color the box plots
        colors = ['lightgreen', 'lightyellow', 'lightcoral']
        for patch, color in zip(bp1['boxes'], colors):
            patch.set_facecolor(color)
        
        ax3.set_ylabel('Time (seconds)', fontsize=11)
        ax3.set_title('Time Distribution by Difficulty', fontsize=12, fontweight='bold')
        ax3.grid(axis='y', alpha=0.3)
        
        # Plot 4: Cells Solved by AC3
        ax4 = axes[1, 1]
        bars4 = ax4.bar(difficulties, avg_cells_solved, yerr=std_cells_solved,
                        capsize=5, alpha=0.7, color=['green', 'orange', 'red'])
        ax4.set_ylabel('Cells Solved', fontsize=11)
        ax4.set_title('Average Cells Solved by AC3', fontsize=12, fontweight='bold')
        ax4.grid(axis='y', alpha=0.3)
        
        # Add value labels on bars
        for bar, val in zip(bars4, avg_cells_solved):
            height = bar.get_height()
            ax4.text(bar.get_x() + bar.get_width()/2., height,
                    f'{val:.1f}', ha='center', va='bottom', fontsize=9)
        
        plt.tight_layout()
        
        # Save the plot
        output_dir = os.path.join(os.path.dirname(__file__), '..', 'assets', 'plots')
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, 'benchmark_comparison.png')
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"\nPlot saved to: {output_path}")
        
        plt.show()
    
    def plot_individual_puzzles(self):
        """Generate scatter plots showing individual puzzle performance."""
        fig, axes = plt.subplots(1, 2, figsize=(14, 5))
        fig.suptitle('Individual Puzzle Performance (AC3)', fontsize=16, fontweight='bold')
        
        colors = {'Easy': 'green', 'Medium': 'orange', 'Hard': 'red'}
        markers = {'Easy': 'o', 'Medium': 's', 'Hard': '^'}
        
        # Plot 1: Time vs Clues
        ax1 = axes[0]
        for difficulty in self.difficulties:
            if not self.results[difficulty]:
                continue
            clues = [r['clues'] for r in self.results[difficulty]]
            times = [r['time'] for r in self.results[difficulty]]
            ax1.scatter(clues, times, c=colors[difficulty], marker=markers[difficulty],
                       label=difficulty, alpha=0.6, s=100, edgecolors='black')
        
        ax1.set_xlabel('Number of Clues', fontsize=11)
        ax1.set_ylabel('Solving Time (seconds)', fontsize=11)
        ax1.set_title('AC3 Solving Time vs Number of Clues', fontsize=12, fontweight='bold')
        ax1.legend()
        ax1.grid(alpha=0.3)
        
        # Plot 2: Domain Reductions vs Clues
        ax2 = axes[1]
        for difficulty in self.difficulties:
            if not self.results[difficulty]:
                continue
            clues = [r['clues'] for r in self.results[difficulty]]
            reductions = [r['domain_reductions'] for r in self.results[difficulty]]
            ax2.scatter(clues, reductions, c=colors[difficulty], marker=markers[difficulty],
                       label=difficulty, alpha=0.6, s=100, edgecolors='black')
        
        ax2.set_xlabel('Number of Clues', fontsize=11)
        ax2.set_ylabel('Domain Reductions', fontsize=11)
        ax2.set_title('Domain Reductions vs Number of Clues', fontsize=12, fontweight='bold')
        ax2.legend()
        ax2.grid(alpha=0.3)
        
        plt.tight_layout()
        
        # Save the plot
        output_dir = os.path.join(os.path.dirname(__file__), '..', 'assets', 'plots')
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, 'individual_puzzles.png')
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"Plot saved to: {output_path}")
        
        plt.show()


def main():
    """Main function to run the benchmark suite."""
    # Create benchmark with 10 puzzles per difficulty
    benchmark = SudokuBenchmark(num_puzzles_per_difficulty=10)
    
    # Run the benchmark
    benchmark.run_benchmark()
    
    # Print statistics
    benchmark.print_statistics()
    
    # Generate plots
    print("\nGenerating plots...")
    benchmark.plot_results()
    benchmark.plot_individual_puzzles()
    
    print("\nBenchmark analysis complete!")


if __name__ == "__main__":
    main()
