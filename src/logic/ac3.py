from collections import deque

def ac3(csp):
    """
    AC-3 Algorithm.
    Returns False if an inconsistency is found (empty domain), True otherwise.
    Updates csp.domains in place.
    """
    queue = deque()
    
    # Initialize queue with all arcs in the CSP [cite: 48]
    for xi in csp.variables:
        for xj in csp.neighbors[xi]:
            queue.append((xi, xj))

    while queue:
        xi, xj = queue.popleft()
        
        if revise(csp, xi, xj):
            if len(csp.domains[xi]) == 0:
                return False  # Inconsistency found
            
            # Add neighbors of Xi (excluding Xj) to queue [cite: 58]
            for xk in csp.neighbors[xi]:
                if xk != xj:
                    queue.append((xk, xi))
    return True

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