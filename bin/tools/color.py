#!/usr/bin/env python3
# vim:fileencoding=ISO-8859-1

class Color:

    def __init__(self, c=None):
        self.red = 0
        self.green = 0
        self.blue = 0

        if isinstance(c, Color):
            self.Color(c)

    def Color(self, c):
        self.red = c.red
        self.green = c.green
        self.blue = c.blue

    def getCopy(self):
        return Color(self)
