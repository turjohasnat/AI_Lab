import json
import copy

class ExamSchedulingCSP:
    """
    Incomplete University Timetabling CSP Solver.
    """
    def __init__(self, courses, domains, course_metadata, consistent):
        self.variables = courses
        # Domain is a list of all possible ((Day, AM/PM), Room) tuples
        self.domains = {c: list(domains) for c in courses}
        self.course_metadata = course_metadata
        self.backtrack_count = 0 
        self.node_visited = 0
        self.consistent = consistent

    def is_consistent(self, variable, value, assignment):
        """
        Validates if assigning 'value' to 'variable' violates any constraints.
        
        Args:
            variable (str): The course being assigned (e.g., 'CSE111').
            value (tuple): The proposed assignment in the form ((Day, AM/PM), Room).
            assignment (dict): The current partial state of assignments.
            
        Returns:
            bool: True if consistent, False if a constraint is violated.
        """
        slot, room = value
        meta = self.course_metadata[variable]
        
        # --- YOUR IMPLEMENTATION REQUIRED ---
        # Currently, this only checks for basic Room Overlaps.
        # You must implement the Unary Lab constraint, Batch conflict, 
        # Invigilator conflict, and the Same-Day Fatigue constraint.

        for meta in self.meta:
            if meta in assignment:
                meta_value = assignment[meta]
                if not self.consistent(
                    variable, value, assignment
                ):   
                    return False
            return True    

        for other_var, other_val in assignment.items():
            other_slot, other_room = other_val
            
            # Basic Room Overlap Constraint
            if slot == other_slot and room == other_room:
                return False
                
        return True

    def mrv_select_variable(self, assignment):
        """
        Selects the next unassigned variable.
        
        Args:
            assignment (dict): The current partial assignment state.
            
        Returns:
            str: The name of the variable (course) to assign next.
        """
        # --- YOUR IMPLEMENTATION REQUIRED ---
        # Currently defaults to Naive chronological selection.
        # You must upgrade this to the Minimum Remaining Values (MRV) heuristic.
        unassigned = [v for v in self.variables if v not in assignment]
        return min (
            unassigned,
            key = lembda v:len(self.domain[v])
        )

    def backtracking_search(self):
        self.node_visited = 0
        return self.backtrack({})

    def backtrack(self, assignment=None):
        """
        Executes depth-first search with backtracking.
        
        Args:
            assignment (dict): The current partial assignment state.
            
        Returns:
            dict: A complete, consistent assignment, or None if no solution exists.
        """
        if assignment is None:
            assignment = {}
            
        # --- YOUR IMPLEMENTATION REQUIRED ---
        # A basic chronological backtracker is provided. 
        # Ensure it properly integrates your MRV function and tracks backtrack counts.
        
        self.node_visited += 1
        if len(assignment) == len(self.variables):
            return assignment.copy()

        var = self.mrv_select_variable(assignment)
        
        for val in self.domains[var]:
            if self.is_consistent(var, val, assignment):
                assignment[var] = val
                
                result = self.backtrack(assignment)
                if result is not None:
                    return result
                
                self.backtrack_count += 1
                del assignment[var]
                
        return None

# =====================================================================
# TEST RUNNER SUITE - DO NOT MODIFY BELOW THIS LINE
# =====================================================================

def run_tests():
    # Define variables
    courses = ['CSE111', 'CSE112', 'CSE221', 'CSE222', 'CSE331', 'CSE332']
    
    # Define time slots: Day 1 & Day 2 (AM and PM)
    time_slots = [(1, 'AM'), (1, 'PM'), (2, 'AM'), (2, 'PM')]
    
    # Define rooms
    rooms = ['Room_101', 'Room_102', 'Lab_401']
    
    # Create absolute domain: Cartesian product of slots and rooms
    domain = [(ts, r) for ts in time_slots for r in rooms]

    # Define Course Metadata
    course_meta = {
        'CSE111': {'batch': 'Batch_1', 'invigilator': 'Prof_Rahman', 'lab_required': True},
        'CSE112': {'batch': 'Batch_1', 'invigilator': 'Dr_Karim',   'lab_required': False},
        'CSE221': {'batch': 'Batch_2', 'invigilator': 'Prof_Rahman', 'lab_required': False},
        'CSE222': {'batch': 'Batch_2', 'invigilator': 'Dr_Hassan',  'lab_required': True},
        'CSE331': {'batch': 'Batch_3', 'invigilator': 'Dr_Karim',   'lab_required': False},
        'CSE332': {'batch': 'Batch_3', 'invigilator': 'Dr_Nahar',   'lab_required': False},
    }

    print("Initializing Exam Scheduling CSP...")
    csp = ExamSchedulingCSP(courses, domain, course_meta)
    
    print("Executing Backtracking Search...")
    solution = csp.backtrack()
    
    # Validation Logic
    if solution is None:
        print("FAIL: No solution returned. Logic is flawed.")
        return
        
    if len(solution) != len(courses):
        print(f"FAIL: Incomplete assignment. Assigned {len(solution)} out of {len(courses)} courses.")
        return

    # Validating Constraints on the Output
    passed = True
    for c, (s, r) in solution.items():
        if course_meta[c]['lab_required'] and 'Lab' not in r:
            print(f"CONSTRAINT VIOLATION: {c} requires a Lab, but was scheduled in {r}.")
            passed = False
        if not course_meta[c]['lab_required'] and 'Lab' in r:
            print(f"CONSTRAINT VIOLATION: {c} does not require a Lab, but was scheduled in {r}.")
            passed = False
            
    solution_items = list(solution.items())
    for i in range(len(solution_items)):
        for j in range(i + 1, len(solution_items)):
            c1, (s1, r1) = solution_items[i]
            c2, (s2, r2) = solution_items[j]
            m1, m2 = course_meta[c1], course_meta[c2]
            
            if s1 == s2 and r1 == r2:
                print(f"CONSTRAINT VIOLATION: Room overlap between {c1} and {c2} in {r1} at {s1}.")
                passed = False
            if s1 == s2 and m1['batch'] == m2['batch']:
                print(f"CONSTRAINT VIOLATION: Batch {m1['batch']} conflict between {c1} and {c2} at {s1}.")
                passed = False
            if s1 == s2 and m1['invigilator'] == m2['invigilator']:
                print(f"CONSTRAINT VIOLATION: Invigilator {m1['invigilator']} conflict between {c1} and {c2} at {s1}.")
                passed = False
            if m1['batch'] == m2['batch'] and s1[0] == s2[0] and s1[1] != s2[1]:
                print(f"CONSTRAINT VIOLATION: Fatigue limit exceeded for {m1['batch']} on Day {s1[0]} ({c1} and {c2}).")
                passed = False

    if passed:
        print("SUCCESS: All constraints met! Valid Timetable Generated:")
        print(json.dumps(solution, indent=4))
        print(f"Nodes expanded (Backtracks): {csp.backtrack_count}")
    else:
        print("TEST FAILED: One or more constraints were violated by the solution.")

if __name__ == "__main__":
    run_tests()
