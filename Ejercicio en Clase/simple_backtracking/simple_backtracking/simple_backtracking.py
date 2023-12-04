from utils import *
class Problem:
    """The abstract class for a formal problem. You should subclass
    this and implement the methods actions and result, and possibly
    __init__, goal_test, and path_cost. Then you will create instances
    of your subclass and solve them with the various search functions."""

    def __init__(self, initial, goal=None):
        """The constructor specifies the initial state, and possibly a goal
        state, if there is a unique goal. Your subclass's constructor can add
        other arguments."""
        self.initial = initial
        self.goal = goal

    def actions(self, state):
        """Return the actions that can be executed in the given
        state. The result would typically be a list, but if there are
        many actions, consider yielding them one at a time in an
        iterator, rather than building them all at once."""
        raise NotImplementedError

    def result(self, state, action):
        """Return the state that results from executing the given
        action in the given state. The action must be one of
        self.actions(state)."""
        raise NotImplementedError

    def goal_test(self, state):
        """Return True if the state is a goal. The default method compares the
        state to self.goal or checks for state in self.goal if it is a
        list, as specified in the constructor. Override this method if
        checking against a single self.goal is not enough."""
        if isinstance(self.goal, list):
            return is_in(state, self.goal)
        else:
            return state == self.goal

    def path_cost(self, c, state1, action, state2):
        """Return the cost of a solution path that arrives at state2 from
        state1 via action, assuming cost c to get up to state1. If the problem
        is such that the path doesn't matter, this function will only look at
        state2. If the path does matter, it will consider c and maybe state1
        and action. The default method costs 1 for every step in the path."""
        return c + 1

    def value(self, state):
        """For optimization problems, each state has a value. Hill Climbing
        and related algorithms try to maximize this value."""
        raise NotImplementedError


# ______________________________________________________________________________



from utils import *

class CSP(Problem):
    def __init__(self, variables, domains, neighbors, constraints):
        super().__init__(initial=None, goal=None)
        self.variables = variables
        self.domains = domains
        self.neighbors = neighbors
        self.constraints = constraints
        
    def is_consistent(self, var, value, assignment):
        """Check if a value is consistent with the current assignment."""
        for neighbor in self.neighbors[var]:
            if neighbor in assignment and not self.constraints(var, value, neighbor, assignment[neighbor]):
                return False
        return True

    def assign(self, var, val, assignment):
        """Add {var: val} to assignment."""
        assignment[var] = val

    def unassign(self, var, assignment):
        """Remove {var: val} from assignment."""
        if var in assignment:
            del assignment[var]

    def display(self, assignment):
        """Show a human-readable representation of the CSP."""
        print(assignment)

    def actions(self, state):
        """Return a list of applicable actions: non-conflicting assignments to an unassigned variable."""
        if len(state) == len(self.variables):
            return []
        else:
            assignment = dict(state)
            var = self.select_unassigned_variable(assignment)
            return [(var, val) for val in self.domains[var] if self.is_consistent(var, val, assignment)]

    def result(self, state, action):
        """Perform an action and return the new state."""
        (var, val) = action
        new_state = dict(state)
        new_state[var] = val
        return new_state

    def goal_test(self, state):
        """The goal is to assign all variables, with all constraints satisfied."""
        return len(state) == len(self.variables) and all(self.is_consistent(var, state[var], state) for var in self.variables)

    def select_unassigned_variable(self, assignment):
        """Selects the first unassigned variable."""
        for var in self.variables:
            if var not in assignment:
                return var

    def backtracking_search(self):
        return self.backtrack({})

    def backtrack(self, assignment):
        if len(assignment) == len(self.variables):
            return assignment
        var = self.select_unassigned_variable(assignment)
        for value in self.domains[var]:
            if self.is_consistent(var, value, assignment):
                self.assign(var, value, assignment)
                result = self.backtrack(assignment)
                if result is not None:
                    return result
                self.unassign(var, assignment)
        return None

# Define the constraints function
def constraints(A, a, B, b):
    if A == 'S' and B == 'A':
        return a <= b
    if A == 'A' and B == 'B':
        return a + 3 <= b
    if A == 'B' and B == 'C':
        return a + 2 <= b
    if A == 'C' and B == 'D':
        return a + 4 <= b
    if A == 'D' and B == 'F':
        return a + 2 <= b
    return True  # If it's not one of the above cases, there's no constraint between A and B

# Set up the problem
variables = ['S', 'A', 'B', 'C', 'D', 'F']
domains = {
    'S': [0],
    'A': list(range(0, 12)),
    'B': list(range(0, 12)),
    'C': list(range(0, 12)),
    'D': list(range(0, 12)),
    'F': [11]
}
neighbors = {
    'S': ['A'],
    'A': ['S', 'B', 'C'],
    'B': ['A', 'C', 'D'],
    'C': ['A', 'B', 'D'],
    'D': ['B', 'C', 'F'],
    'F': ['D']
}

# Instantiate the CSP
csp = CSP(variables, domains, neighbors, constraints)

# Perform backtracking search and print the result
result = csp.backtracking_search()
print(result)

