#!/usr/bin/env python3
# vim:fileencoding=ISO-8859-1

# Initialize the program and modules

try:
    import argparse
    from PIL import Image
    import math
    from os import path
except ImportError as err:
    print("Could not load {} module.".format(err))
    raise SystemExit

from utilities import Utilities

class TileSet:

    def __init__(self):
        self.image = False
        self.tileData = False
        self.tileSet = False

    def processImage(self, image):
        if isinstance(image, str):
            self.image = Utilities.loadImage(image)
        elif hasattr(image, 'width'):
            self.image = image

        if self.image == False:
            return False

        # Extract Tileset
        self.tileData = Utilities.readImageTiles(self.image)
        self.tileSet = Utilities.extractTileSet(self.tileData)

        return self.tileSet

    def getTileSet(self):
        return self.tileSet

    def composeHeader(self, file, label):
        # Process output file name
        file = path.splitext(file)[0] # Remove extension
        filename = path.basename(file) # Get name

        if self.tileSet == False:
            return False

        # Compose Header File Output
        h_output = "#ifndef {}_H_\n".format(filename.upper())
        h_output += "#define {}_H_\n\n".format(filename.upper())
        h_output += "#include <stdint.h>\n\n"
        h_output += "#define MAXTILEINDEX {:d}\n".format(len(self.tileSet))
        h_output += "#define TILESIZEX {:d}\n".format(Utilities.tileSize)
        h_output += "#define TILESIZEY {:d}\n".format(Utilities.tileSize)
        h_output += "extern const uint8_t {}[MAXTILEINDEX][TILESIZEX * TILESIZEY];\n\n".format(label)
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

        if self.tileSet == False:
            return False

        # Compose C File Output
        c_output = "#include \"{}.h\"\n\n".format(filename)
        c_output += "const uint8_t {}[MAXTILEINDEX][TILESIZEX * TILESIZEY] = {{\n".format(label)

        for i in range(0, len(self.tileSet)):
            c_output += " " * Utilities.outputTabLength + "{\n"

            for y in range(0, Utilities.tileSize):
                c_output += " " * (Utilities.outputTabLength * 2)
                for x in range(0, Utilities.tileSize):
                    c_output += "0x{:02X}".format(self.tileSet[i][y][x])
                    if x < Utilities.tileSize - 1:
                        c_output += ", "
                if y < Utilities.tileSize - 1:
                    c_output += ","
                c_output += "\n"

            c_output += " " * Utilities.outputTabLength + "}"
            if i < len(self.tileSet) - 1:
                c_output += ","
            c_output += "\n"

        c_output += "};\n"

        # Save C File
        codeFile = open("{}.c".format(file), "w")
        codeFile.write(c_output)
        codeFile.close()

class TileSetCLI:

    def __init__(self):
        # Parse command line arguments
        parser = argparse.ArgumentParser()
        parser.add_argument("-v", "--verbose", help="display more verbose information", action="store_true")
        parser.add_argument("-l", "--label", help="variable label to use in your code", default="tileData")
        parser.add_argument("-i", "--infile", help="location to read image file (jpg/png/bmp)")
        parser.add_argument("-o", "--outfile", help="name and location of .c and .h file (don't include file extension)", default="tileset")

        self.args = parser.parse_args()
        if self.args.infile == None:
            print("No image specified.")
            raise SystemExit

        if self.args.verbose:
            print("uSVC Tileset Converter - Version 0.10")

        # Read Image
        image = Utilities.loadImage(self.args.infile)
        if self.args.verbose:
            print("Image successfully loaded.")
            Utilities.printImageInfo(image)

        self.tileSet = TileSet()
        self.tileSet.processImage(image)

        self.tileSet.composeHeader(self.args.outfile, self.args.label)
        self.tileSet.composeCode(self.args.outfile, self.args.label)

        if self.args.verbose:
            print("Successfully converted image to tileset data. {:d} tiles in tileset.".format(len(tileset)))

        raise SystemExit

if __name__ == "__main__":
    TileSetCLI();
