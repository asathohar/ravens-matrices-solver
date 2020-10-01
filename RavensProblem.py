# A single Raven's Progressive Matrix problem, represented by a type (2x2
# or 3x3), a String name, and a dictionary of figures.
class RavensProblem:
    # Initializes a new Raven's Progressive Matrix problem given a name, a
    # type, and a correct answer to the problem. Also initializes a blank
    # dictionary representing the figures in the problem.
    def __init__(self, name, problemType, problemSetName, hasVisual, hasVerbal):

        self.name=name

        self.problemType=problemType

        self.problemSetName = problemSetName

        self.hasVisual=hasVisual

        self.hasVerbal=hasVerbal

        self.figures={}

