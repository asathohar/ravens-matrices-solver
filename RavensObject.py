# A single object in a RavensFigure -- typically, a single shape in a frame,
# such as a triangle or a circle -- comprised of a list of name-value attributes.
class RavensObject:
    # Constructs a new RavensObject given a name.
    # @param name the name of the object
    def __init__(self, name):
        self.name=name

        self.attributes={}