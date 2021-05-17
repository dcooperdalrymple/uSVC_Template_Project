#!/usr/bin/env python3
# vim:fileencoding=ISO-8859-1

from color import Color

class Palette:

    initialized = False

    uChipVGAred = [0 for i in range(0, 256)]
    uChipVGAgreen = [0 for i in range(0, 256)]
    uChipVGAblue = [0 for i in range(0, 256)]

    def __init__(self):
        pass

    # Must call this function before using palette
    @staticmethod
    def calculate():
        if Palette.initialized == True:
            return

        redGreenThresholds = [(0 + 32)/2, (32 + 71) / 2, (71 + 103) / 2, (103 + 151) / 2, (151 + 184) / 2, (184 + 222) / 2, (222 + 255) / 2]
        blueThresholds = [(0 + 86) / 2, (86 + 180) / 2, (180 + 255) / 2]

        for i in range(0, 256):

            if i > redGreenThresholds[6]:
                Palette.uChipVGAred[i] = 7
                Palette.uChipVGAgreen[i] = 7
            elif i > redGreenThresholds[5]:
                Palette.uChipVGAred[i] = 6
                Palette.uChipVGAgreen[i] = 6
            elif i > redGreenThresholds[4]:
                Palette.uChipVGAred[i] = 5
                Palette.uChipVGAgreen[i] = 5
            elif i > redGreenThresholds[3]:
                Palette.uChipVGAred[i] = 4
                Palette.uChipVGAgreen[i] = 4
            elif i > redGreenThresholds[2]:
                Palette.uChipVGAred[i] = 3
                Palette.uChipVGAgreen[i] = 3
            elif i > redGreenThresholds[1]:
                Palette.uChipVGAred[i] = 2
                Palette.uChipVGAgreen[i] = 2
            elif i > redGreenThresholds[0]:
                Palette.uChipVGAred[i] = 1
                Palette.uChipVGAgreen[i] = 1
            else:
                Palette.uChipVGAred[i] = 0
                Palette.uChipVGAgreen[i] = 0

            if i > blueThresholds[2]:
                Palette.uChipVGAblue[i] = 3
            elif i > blueThresholds[1]:
                Palette.uChipVGAblue[i] = 2
            elif i > blueThresholds[0]:
                Palette.uChipVGAblue[i] = 1
            else:
                Palette.uChipVGAblue[i] = 0

        Palette.initialized = True

    @staticmethod
    def isCalculated():
        return Palette.initialized == True

    @staticmethod
    def getRed(value):
        return Palette.uChipVGAred[value & 0xFF]

    @staticmethod
    def getGreen(value):
        return Palette.uChipVGAgreen[value & 0xFF]

    @staticmethod
    def getBlue(value):
        return Palette.uChipVGAblue[value & 0xFF]

    @staticmethod
    def getColor(red, green, blue):
        c = Color()
        c.red = Palette.getRed(red)
        c.green = Palette.getGreen(green)
        c.blue = Palette.getBlue(blue)
        return c

    @staticmethod
    def USVCRGBto8bit(red, green, blue):
        return ((red & 1) | ((red & 4) >> 1) | ((red & 2) << 1)  | ((blue & 1) << 3) | ((green & 1) << 4) | ((blue & 2) << 4) | ((green & 2) << 5) | ((green & 4) << 5))

    @staticmethod
    def USVCRGBtoRGB24(r, g, b):
        rgValues = [0, 32, 71, 103, 151, 184, 222, 255]
        bValues = [0, 86, 180, 255]
        return (rgValues[r & 0b0111] << 16) | (rgValues[g & 0b0111] << 8) | bValues[b & 0b0011]

    @staticmethod
    def getByte(pixel):
        c = Palette.getColor(pixel[0], pixel[1], pixel[2])
        return Palette.USVCRGBto8bit(c.red, c.green, c.blue)
