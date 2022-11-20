import sys

from crossword import *

import random # TODO remove

class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        w, h = draw.textsize(letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        for variable in self.crossword.variables:
            for word in self.domains[variable].copy():
                if len(word) != variable.length:
                    self.domains[variable].remove(word)
                

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        revision = False
        for word in self.domains[x].copy():
            if self.crossword.overlaps[x, y] is None:
                continue
            i, j = self.crossword.overlaps[x, y]
            possible = False
            for other_word in self.domains[y]:
                if word[i] == other_word[j]:
                    possible = True
                    break
            if not possible:
                self.domains[x].remove(word)
                revision = True
        return revision

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        if arcs is not None:
            queue = arcs
        else:
            queue = []
            for variable_pair, overlap in self.crossword.overlaps.items():
                if overlap is not None:
                    queue.append(variable_pair)
        while len(queue) != 0:
            x, y = queue.pop(0)
            if self.revise(x, y):
                if len(self.domains[x]) == 0:
                    return False
                for z in self.crossword.neighbors(x):
                    if z != y:
                        queue.append((z, x))
        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        return set(assignment.keys()) == self.crossword.variables

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        print("assignment keys as set: {}".format(set(assignment.keys())))
        if len(assignment.values()) != len(set(assignment.values())):
            return False # i.e. not all values distinct
        for variable, value in assignment.items():
            if variable.length != len(value): 
                return False # i.e. wrong length
        for variable in assignment:
            for neighbouring_variable in self.crossword.neighbors(variable):
                i, j = self.crossword.overlaps[variable, neighbouring_variable]
                if neighbouring_variable in assignment and assignment[variable][i] != assignment[neighbouring_variable][j]:
                    return False # i.e. conflict between characters
        return True

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        num_others_ruled_out = {}
        for val in self.domains[var]:
            n = 0
            for neighbour in self.crossword.neighbors(var):
                if neighbour in assignment:
                    continue
                overlap = self.crossword.overlaps[var, neighbour]
                if overlap is not None:
                    for other_val in self.domains[neighbour]:
                        if val[overlap[0]] != val[overlap[1]]:
                            n += 1
            num_others_ruled_out[val] = n
        return sorted(list(self.domains[var]), key=lambda word: num_others_ruled_out[word])

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        unassigneds = self.crossword.variables - set(assignment.keys())
        domain_size = {}
        for var in unassigneds:
            domain_size[var] = len(self.domains[var])
        min_remaining = min(domain_size.values())
        variables_min_domain = [v for v in domain_size if domain_size[v] == min_remaining]
        if len(variables_min_domain) == 1:
            return variables_min_domain[0]
        degree = {}
        for var in variables_min_domain:
            degree[var] = len(self.crossword.neighbors(var))
        max_degree = max(degree.values())
        variables_max_degree = [v for v in degree if degree[v] == max_degree]
        return variables_max_degree[0]
        # return random.choice(list(self.crossword.variables - set(assignment.keys())))
        # TODO -- implement minimum remaining value heuristic and then degree heuristic

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        if self.assignment_complete(assignment):
            return assignment
        unassigned_variable = self.select_unassigned_variable(assignment)
        for word in self.domains[unassigned_variable]:
            new_assignment = assignment.copy()
            new_assignment[unassigned_variable] = word
            if self.consistent(new_assignment):
                result = self.backtrack(new_assignment) # might need changing
                if result is not None:
                    return result
        return None
                
            # TODO
            

def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
