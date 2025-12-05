from collections import deque
import numpy as np
import copy
import os
from datetime import datetime

def ac3(csp, log_steps=False, log_file=None):
    """
    AC-3 Algorithm.
    Returns (success, board_states) tuple.
    - success: False if an inconsistency is found (empty domain), True otherwise.
    - board_states: List of board snapshots captured when domains become singletons.
    Updates csp.domains in place.
    
    Args:
        csp: The constraint satisfaction problem
        log_steps: If True, logs detailed information
        log_file: Path to log file. If None and log_steps=True, creates 'ac3_log_<timestamp>.txt'
    """
    queue = deque()
    board_states = []  # Store board states when singletons are found
    step_count = 0
    
    # Setup logging
    log_handle = None
    if log_steps:
        if log_file is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            log_file = f"ac3_log_{timestamp}.txt"
        log_handle = open(log_file, 'w', encoding='utf-8')
    
    # Initialize queue with all arcs in the CSP
    for xi in csp.variables:
        for xj in csp.neighbors[xi]:
            queue.append((xi, xj))

    # Log initial domains
    if log_steps:
        _log_to_file(log_handle, "\n=== AC-3 Initial State ===")
        _log_domains(csp, step_count, log_handle)
    
    # Capture initial board state
    current_board = _create_board_snapshot(csp)
    board_states.append(current_board.copy())

    while queue:
        xi, xj = queue.popleft()
        step_count += 1
        
        if revise(csp, xi, xj):
            if len(csp.domains[xi]) == 0:
                if log_steps:
                    _log_to_file(log_handle, f"\n=== AC-3 Failed at Step {step_count} ===")
                    _log_to_file(log_handle, f"Domain of {xi} became empty!")
                    log_handle.close()
                return False, board_states  # Inconsistency found
            
            # Log domains after revision
            if log_steps:
                _log_to_file(log_handle, f"\n=== AC-3 Step {step_count} ===")
                _log_to_file(log_handle, f"Revised arc: {xi} -> {xj}")
                _log_domains(csp, step_count, log_handle)
            
            # Check if any domain became singleton and update board
            if len(csp.domains[xi]) == 1:
                current_board = _create_board_snapshot(csp)
                board_states.append(current_board.copy())
                if log_steps:
                    _log_to_file(log_handle, f">>> Singleton found at {xi}: value = {csp.domains[xi][0]}")
                    _log_to_file(log_handle, f">>> Board state saved (total states: {len(board_states)})")
            
            # Add neighbors of Xi (excluding Xj) to queue
            for xk in csp.neighbors[xi]:
                if xk != xj:
                    queue.append((xk, xi))
    
    if log_steps:
        _log_to_file(log_handle, f"\n=== AC-3 Completed Successfully ===")
        _log_to_file(log_handle, f"Total steps: {step_count}")
        _log_to_file(log_handle, f"Total board states captured: {len(board_states)}")
        _log_domains(csp, step_count, log_handle, final=True)
        log_handle.close()
        print(f"AC-3 log saved to: {log_file}")
    
    return True, board_states

def revise(csp, xi, xj):
    """
    Returns True iff we revise the domain of Xi.
    Removes x from Xi's domain if no value y in Xj allows (x,y) to satisfy constraint[cite: 56, 57].
    """
    revised = False
    # In Sudoku, if Xj has a specific single value, Xi cannot be that value.
    if len(csp.domains[xj]) == 1:
        val_j = csp.domains[xj][0]
        if val_j in csp.domains[xi]:
            csp.domains[xi].remove(val_j)
            revised = True
    return revised

def _log_to_file(file_handle, message):
    """
    Writes a message to the log file.
    """
    if file_handle:
        file_handle.write(message + "\n")
        file_handle.flush()

def _log_domains(csp, step, log_handle=None, final=False):
    """
    Logs the current state of all domains.
    """
    if final:
        _log_to_file(log_handle, "\n--- Final Domain State ---")
    else:
        _log_to_file(log_handle, f"\n--- Domain State (Step {step}) ---")
    
    # Count singletons and empty cells
    singletons = []
    multi_domain = []
    
    for var in sorted(csp.variables):
        domain = csp.domains[var]
        if len(domain) == 1:
            singletons.append(var)
        elif len(domain) > 1:
            multi_domain.append((var, domain))
    
    _log_to_file(log_handle, f"Singletons: {len(singletons)}/81")
    _log_to_file(log_handle, f"Multi-domain cells: {len(multi_domain)}")
    
    # Show some multi-domain cells (first 10)
    if multi_domain:
        _log_to_file(log_handle, "\nSample multi-domain cells:")
        for var, domain in multi_domain[:10]:
            _log_to_file(log_handle, f"  {var}: {domain}")
        if len(multi_domain) > 10:
            _log_to_file(log_handle, f"  ... and {len(multi_domain) - 10} more")

def _create_board_snapshot(csp):
    """
    Creates a 9x9 numpy array snapshot of the current board state.
    Cells with singleton domains are filled, others remain 0.
    """
    board = np.zeros((9, 9), dtype=int)
    for r in range(9):
        for c in range(9):
            if len(csp.domains[(r, c)]) == 1:
                board[r, c] = csp.domains[(r, c)][0]
    return board