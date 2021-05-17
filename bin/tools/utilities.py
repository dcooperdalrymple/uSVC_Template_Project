#!/usr/bin/env python3
# vim:fileencoding=ISO-8859-1

try:
    import math
    from PIL import Image
except ImportError as err:
    print("Could not load {} module.".format(err))
    raise SystemExit

from palette import Palette

class Utilities:

    # uSVC VGA Pixel Constants
    pixelAndMask = 0b1100000011001111
    pixelOrMask = 1 << 9 # Disable SDCS
    pixelMulFactor = 1024 + 1 # Convert a uSVC encoded color byte to its signals

    # Tile Constants
    tileSize = 8

    # Code File Output Constants
    outputTabLength = 4

    def __init__(self):
        pass

    @staticmethod
    def bytesToHex(bytes):
        hexChars = ''
        for i in range(0, len(bytes)):
            hexChars += "{0:0{1}x}".format(bytes[i] & 0xFF, 2)
        return hexChars

    @staticmethod
    def USVCpixelToSignals(pixel):
        # Pixel uSVC encoded!
        return (Utilities.pixelOrMask | ((Utilities.pixelMulFactor * pixel) & Utilities.pixelAndMask))

    @staticmethod
    def USVCbiPixelToSignals(bipixel):
        return self.USVCpixelToSignals(bipixel & 0xFF) | (self.USVCpixelToSignals((bipixel >> 8)) << 16)

    @staticmethod
    def createCFileArrayString(arrayName, array, elementSize, maxElementsPerLine, unsigned, constant):
        if elementSize == 1:
            mask = 0xFF
            arrayType = "int8_t"
        elif elementSize == 2:
            mask = 0xFFFF
            arrayType = "int16_t"
        else:
            elementSize = 4
            mask = 0xFFFFFFFF
            arrayType = "int32_t"

        sb = ""
        if constant:
            sb += "const "
        if unsigned:
            sb += "u"
        sb += arrayType + " " + arrayName + "[" + len(array) + "] = \r\n{\n\t"

        for i in range(0, len(array)):
            sb += "{0:0{1}x}".format(array[i] & mask, elementSize * 2)
            if i < len(array) - 1:
                sb += ", "
                if i % maxElementsPerLine == (maxElementsPerLine - 1):
                    sb += "\r\n\t"
            else:
                sb += "\r\n};\r\n"

        return sb

    @staticmethod
    def loadImage(name):
        image = Image.open(name).convert('RGB')
        return image

    @staticmethod
    def printImageInfo(image):
        print("Width: {:d}px".format(image.width))
        print("Height: {:d}px".format(image.height))
        print("Tiles W: {:d}".format(Utilities.getImageTileW(image)))
        print("Tiles H: {:d}".format(Utilities.getImageTileH(image)))

    @staticmethod
    def getImageBuffer(image, width = -1, height = -1):
        if Palette.isCalculated() == False:
            Palette.calculate()

        if width < 0 or width > image.width:
            width = image.width
        if height < 0 or height > image.height:
            height = image.height

        width = int(math.floor(width / Utilities.tileSize) * Utilities.tileSize)
        height = int(math.floor(height / Utilities.tileSize) * Utilities.tileSize)

        buffer = [0 for i in range(0, width * height)]

        for i in range(0, width * height):
            x = i % width
            y = int(math.floor(i / width))

            tile = int(math.floor(x / Utilities.tileSize) + math.floor(y / Utilities.tileSize) * math.floor(width / Utilities.tileSize))
            tileX = x % Utilities.tileSize
            tileY = y % Utilities.tileSize
            buffer[tile * Utilities.tileSize * Utilities.tileSize + tileY * Utilities.tileSize + tileX] = Palette.getByte(image.getpixel((x, y)))

        return buffer

    # Binary data in units of 4 bytes
    @staticmethod
    def calculateCheckSum(data):
        sum = 0
        for i in range(0, int(math.floor(len(data) / 4))):
            b0 = 0xFF & data[i * 4]
            b1 = 0xFF & data[(i * 4) + 1]
            b2 = 0xFF & data[(i * 4) + 2]
            b3 = 0xFF & data[(i * 4) + 3]
            sum += b0 | (b1 << 8) | (b2 << 16) | (b3 << 24)
        return sum

    @staticmethod
    def getImageTileW(image):
        return int(math.floor(image.width / float(Utilities.tileSize)))

    @staticmethod
    def getImageTileH(image):
        return int(math.floor(image.height / float(Utilities.tileSize)))

    @staticmethod
    def readImageTiles(image):
        if Palette.isCalculated() == False:
            Palette.calculate()

        tileW = int(math.floor(image.width / float(Utilities.tileSize)))
        tileH = int(math.floor(image.height / float(Utilities.tileSize)))
        tileLen = tileW * tileH

        tileData = [[[0 for x in range(0, Utilities.tileSize)] for y in range(0, Utilities.tileSize)] for i in range(0, tileLen)]

        for y in range(0, tileH):
            for x in range(0, tileW):
                for i in range(0, Utilities.tileSize):
                    for j in range(0, Utilities.tileSize):
                        tileData[y * tileW + x][i][j] = Palette.getByte(image.getpixel((x * Utilities.tileSize + j, y * Utilities.tileSize + i)))

        return tileData

    @staticmethod
    def equalTiles(tileA, tileB):
        for y in range(0, Utilities.tileSize):
            for x in range(0, Utilities.tileSize):
                if int(tileA[y][x]) != int(tileB[y][x]):
                    return False
        return True

    @staticmethod
    def extractTileSet(tileData):
        tileSet = []

        for i in range(0, len(tileData)):
            found = False

            for j in range(0, len(tileSet)):
                if Utilities.equalTiles(tileData[i], tileSet[j]) == True:
                    found = True
                    break

            if found == False:
                tileSet.append(tileData[i])

        return tileSet

    @staticmethod
    def getTileMap(tileData, tileSet):
        tilemap = [0 for i in range(0, len(tileData))]

        for i in range(0, len(tileData)):
            for j in range(0, len(tileSet)):
                if Utilities.equalTiles(tileData[i], tileSet[j]) == True:
                    tilemap[i] = j
                    break

        return tilemap
