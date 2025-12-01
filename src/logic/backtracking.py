def backtracking_search(csp):
    """
    Main entry for backtracking search.
    Returns a complete assignment or None if failure.
    """
    # Create initial assignment from the current state of domains/board
    # We trust AC-3 has already reduced domains, so we can use singletons
    assignment = {}
    for var in csp.variables:
        if len(csp.domains[var]) == 1:
            assignment[var] = csp.domains[var][0]
            
    return backtrack(assignment, csp)

def backtrack(assignment, csp):
    """Recursive backtracking function."""
    if len(assignment) == len(csp.variables):
        return assignment  # Solution found

    var = select_unassigned_variable(assignment, csp)
    
    # Order domain values: using the reduced domains from AC-3
    for value in csp.domains[var]:
        if csp.is_consistent(var, value, assignment):
            assignment[var] = value
            result = backtrack(assignment, csp)
            if result:
                return result
            del assignment[var]
            
    return None

def select_unassigned_variable(assignment, csp):
    """Selects the next variable to assign (Simple: first empty found)."""
    for var in csp.variables:
        if var not in assignment:
            return var
    return None