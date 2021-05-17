#!/usr/bin/env python3
# vim:fileencoding=ISO-8859-1

# Initialize the program and modules

try:
    import sys
    import argparse
    from PIL import Image
    import math
    from os import path
except ImportError as err:
    print("Could not load {} module.".format(err))
    raise SystemExit

from utilities import Utilities

class TileMap:

    def __init__(self):
        self.image = False
        self.tileW = 0
        self.tileH = 0
        self.tileData = False
        self.tileSet_image = False
        self.tileSet_data = False
        self.tileSet = False
        self.tileMap = False

    def processImage(self, image, tileSet = False):
        if isinstance(image, str):
            self.image = Utilities.loadImage(image)
        elif hasattr(image, 'width'):
            self.image = image

        if self.image == False:
            return False

        # Get tiles from image
        self.tileW = Utilities.getImageTileW(image)
        self.tileH = Utilities.getImageTileH(image)
        self.tileData = Utilities.readImageTiles(image)

        # Determine tileset
        if tileSet == False:
            self.tileSet = Utilities.extractTileSet(self.tileData)
        elif isinstance(tileSet, str):
            self.tileSet_image = Utilities.loadImage(tileSet)
            self.tileSet_data = Utilities.readImageTiles(self.tileSet_image)
            self.tileSet = Utilities.extractTileSet(self.tileSet_data)
        elif isinstance(tileSet, Image):
            self.tileSet_image = tileSet
            self.tileSet_data = Utilities.readImageTiles(self.tileSet_image)
            self.tileSet = Utilities.extractTileSet(self.tileSet_data)
        elif isinstance(tileSet, list):
            self.tileSet = tileSet

        if self.tileSet == False:
            return False

        # Identify tiles in tileset to build tilemap
        self.tileMap = Utilities.getTileMap(self.tileData, self.tileSet)

        return self.tileMap

    def getTileMap(self):
        return self.tileMap

    def composeHeader(self, file, label):
        # Process output file name
        file = path.splitext(file)[0] # Remove extension
        filename = path.basename(file) # Get name

        if self.tileMap == False:
            return False

        # Compose Header File Output
        h_output = "#ifndef {}_H_\n".format(filename.upper())
        h_output += "#define {}_H_\n\n".format(filename.upper())
        h_output +=  "#include <stdint.h>\n\n"
        h_output += "#define MAPSIZEX_{} {:d}\n".format(label.upper(), self.tileW)
        h_output += "#define MAPSIZEY_{} {:d}\n".format(label.upper(), self.tileH)
        h_output += "extern const uint16_t {}[MAPSIZEY_{} * MAPSIZEX_{}];\n\n".format(label, label.upper(), label.upper())
        h_output += "#endif\n"

        # Save Header File
        headerFile = open("{}.h".format(file), "w")
        headerFile.write(h_output)
        headerFile.close()

        return True

    def composeCode(self, file, label):
        # Process output file name
        file = path.splitext(file)[0] # Remove extension
        filename = path.basename(file) # Get name

        if self.tileMap == False:
            return False

        # Compose C File Output
        c_output = "#include \"{}.h\"\n\n".format(filename)
        c_output += "const uint16_t {}[MAPSIZEY_{} * MAPSIZEX_{}] = {{\n".format(label, label.upper(), label.upper())

        for y in range(0, self.tileH):
            c_output += " " * Utilities.outputTabLength
            for x in range(0, self.tileW):
                c_output += "0x{:04X}".format(self.tileMap[y * self.tileW + x])
                if x < self.tileW - 1:
                    c_output += ", "
            if y < self.tileH - 1:
                c_output += ","
            c_output += "\n"
        c_output += "};\n"

        # Save C File
        codeFile = open("{}.c".format(file), "w")
        codeFile.write(c_output)
        codeFile.close()

        return True

class TileMapCLI:

    def __init__(self):
        # Parse command line arguments
        parser = argparse.ArgumentParser()
        parser.add_argument("-v", "--verbose", help="display more verbose information", action="store_true")
        parser.add_argument("-l", "--label", help="variable label to use in your code", default="tileMap")
        parser.add_argument("-i", "--infile", help="location to read image file (jpg/png/bmp)")
        parser.add_argument("-o", "--outfile", help="name and location of .c and .h file (don't include file extension)", default="tilemap")
        parser.add_argument("-t", "--tilesetfile", help="location to read tileset data (jpg/png/bmp; if not specified, tileset will be extract from infile)")

        self.args = parser.parse_args()

        if self.args.infile == None:
            print("No image specified.")
            raise SystemExit

        if self.args.tilesetfile == None:
            self.args.tilesetfile = False

        if self.args.verbose:
            print("uSVC Tilemap Converter - Version 0.10")

        # Read Image
        image = Utilities.loadImage(self.args.infile)
        if self.args.verbose:
            print("Image successfully loaded")
            Utilities.printImageInfo(image)

        self.tileMap = TileMap()
        self.tileMap.processImage(image, self.args.tilesetfile)

        self.tileMap.composeHeader(self.args.outfile, self.args.label)
        self.tileMap.composeCode(self.args.outfile, self.args.label)

        if self.args.verbose:
            print("Successfully converted image to tilemap data.")

        raise SystemExit

if __name__ == "__main__":
    TileMapCLI()
