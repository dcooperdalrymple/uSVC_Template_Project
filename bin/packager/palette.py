#!/usr/bin/env python3
# vim:fileencoding=ISO-8859-1

from color import USVCColor
from utilities import Utilities

class USVCPalette:

    def __init__(self):
        self.uChipVGAred = [0 for i in range(0, 256)]
        self.uChipVGAgreen = [0 for i in range(0, 256)]
        self.uChipVGAblue = [0 for i in range(0, 256)]

        self.calculate8BitPalette()

    def calculate8BitPalette(self):
        redGreenThresholds = [(0 + 32)/2, (32 + 71) / 2, (71 + 103) / 2, (103 + 151) / 2, (151 + 184) / 2, (184 + 222) / 2, (222 + 255) / 2]
        blueThresholds = [(0 + 86) / 2, (86 + 180) / 2, (180 + 255) / 2]

        for i in range(0, 256):

            if i > redGreenThresholds[6]:
                self.uChipVGAred[i] = 7
                self.uChipVGAgreen[i] = 7
            elif i > redGreenThresholds[5]:
                self.uChipVGAred[i] = 6
                self.uChipVGAgreen[i] = 6
            elif i > redGreenThresholds[4]:
                self.uChipVGAred[i] = 5
                self.uChipVGAgreen[i] = 5
            elif i > redGreenThresholds[3]:
                self.uChipVGAred[i] = 4
                self.uChipVGAgreen[i] = 4
            elif i > redGreenThresholds[2]:
                self.uChipVGAred[i] = 3
                self.uChipVGAgreen[i] = 3
            elif i > redGreenThresholds[1]:
                self.uChipVGAred[i] = 2
                self.uChipVGAgreen[i] = 2
            elif i > redGreenThresholds[0]:
                self.uChipVGAred[i] = 1
                self.uChipVGAgreen[i] = 1
            else:
                self.uChipVGAred[i] = 0
                self.uChipVGAgreen[i] = 0

            if i > blueThresholds[2]:
                self.uChipVGAblue[i] = 3
            elif i > blueThresholds[1]:
                self.uChipVGAblue[i] = 2
            elif i > blueThresholds[0]:
                self.uChipVGAblue[i] = 1
            else:
                self.uChipVGAblue[i] = 0

    def getRed(self, value):
        return self.uChipVGAred[value & 0xFF]

    def getGreen(self, value):
        return self.uChipVGAgreen[value & 0xFF]

    def getBlue(self, value):
        return self.uChipVGAblue[value & 0xFF]

    def getColor(self, red, green, blue):
        c = USVCColor()
        c.red = self.getRed(red)
        c.green = self.getGreen(green)
        c.blue = self.getBlue(blue)
        return c

    def getByte(self, pixel):
        c = self.getColor(pixel[0], pixel[1], pixel[2])
        return Utilities.USVCRGBto8bit(c.red, c.green, c.blue)
