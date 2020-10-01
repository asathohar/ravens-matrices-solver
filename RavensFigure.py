# A single figure in a Raven's Progressive Matrix problem, comprised of a name
# and a list of RavensObjects.

import os

class RavensFigure:
    # Creates a new figure for a Raven's Progressive Matrix given a name.
    # @param name the name of the figure
    def __init__(self, name, problemName, setName):
        self.name=name

        self.objects={}

        self.visualFilename="Problems" + os.sep + setName + os.sep + problemName + os.sep + name + ".png"