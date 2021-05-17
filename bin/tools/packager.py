#!/usr/bin/env python3
# vim:fileencoding=ISO-8859-1
#
# Title: uSVC USC Packager
# Author: D Cooper Dalrymple
# Created: 2021-05-12
# Updated: 2021-05-12
# https://dcdalrymple.com/
#
# Based on https://github.com/next-hack/uChipGameMapEditor/
# Requires Python 3.0 or later

try:
    import sys
    import math
    from os import path
except ImportError as err:
    print("Could not load {} module.".format(err))
    raise SystemExit

from utilities import Utilities
from color import Color
from palette import Palette

class Packager:

    USVCHEADER = "USVC"
    version = "0.0"
    PREVIEW_WIDTH = 96
    PREVIEW_HEIGHT = 72
    AUTHOR_LENGTH = 14
    SHORT_TITLE_LENGTH = 20
    LONG_TITLE_LENGTH = 14
    DESCRIPTION_LENGTH = 14
    DATE_LENGTH = 8
    VERSION_LENGTH = 5

    def __init__(self):
        Palette.calculate()

    def convertToUSVCPreview(self, image):
        buffer = Utilities.getImageBuffer(image, self.PREVIEW_WIDTH, self.PREVIEW_HEIGHT)
        return buffer

    def createPackage(self, binFilePath, metaFilePath, imageFilePath, outputFilePath):
        checkSum = 0
        error = 0

        shortTitle = ""
        longTitle = ["" for i in range(0, 4)]
        description = ["" for i in range(0, 4)]
        authors = ["" for i in range(0, 2)]
        date = ""
        version = ""

        # Read Meta File
        try:
            br = open(metaFilePath, mode="r")

            shortTitle = br.readline().rstrip()
            print("Short Title: \"{}\"".format(shortTitle))

            for i in range(0, len(longTitle)):
                longTitle[i] = br.readline().rstrip()
                print("Long Title Row {:d}: \"{}\"".format(i + 1, longTitle[i]))

            for i in range(0, len(description)):
                description[i] = br.readline().rstrip()
                print("Description Row {:d}: \"{}\"".format(i + 1, description[i]))

            for i in range(0, len(authors)):
                authors[i] = br.readline().rstrip()
                print("Authors Row {:d}: \"{}\"".format(i + 1, authors[i]))

            date = br.readline().rstrip()
            print("Date: \"{}\"".format(date))

            version = br.readline().rstrip()
            print("Version: \"{}\"".format(version))

        except IOError as err:
            print("Could not read meta file, {}: {}.".format(metaFilePath, err))
            error = 1

        # Read Binary File
        try:
            binData = open(binFilePath, mode="rb").read()

            # For simplicity copy binData to a 4-byte aligned array
            tmpBin = [0 for i in range(0, int(4 * math.floor((len(binData) + 3) / 4)))]
            for i in range(0, len(binData)):
                tmpBin[i] = binData[i]
            binData = tmpBin

            # Calculate checksum
            checkSum = Utilities.calculateCheckSum(binData)

        except IOError as err:
            print("Could not read bin file, {}: {}.".format(binFilePath, err))
            error = 1

        # Read Preview Image
        try:
            imgData = self.convertToUSVCPreview(Utilities.loadImage(imageFilePath))
        except IOError as err:
            print("Could not read specified image, {}: {}".format(imageFilePath, err))
            error = 1

        if error == 0:

            # Calculate USC file length
            uscLength = int(512 + 512 * math.floor((self.PREVIEW_WIDTH * self.PREVIEW_HEIGHT + 511) / 512) + len(binData))
            print("Final USC file size: {:d}".format(uscLength))
            finalUSC = [0 for i in range(0, uscLength)]

            # "USVC" 4 bytes header
            # Checksum (4 byte, binary little endian)
            # Bin Length (4 byte, binary little endian)
            # Paddings (20 bytes)
            # Short Title (32 chars)
            # Long Titles (4 x 32 chars)
            # Description (4 x 32 chars)
            # Authonrs (2 x 32 chars)
            # date (32 chars)
            # version (32 chars)
            # paddings (64 bytes)
            # 13 sectors for the preview image
            # 0.5 sector for the preview image
            # 0.5 sector Paddings
            # binary file

            # Copy header @0
            cur = 0
            for i in range(0, len(self.USVCHEADER)):
                finalUSC[i] = self.USVCHEADER.encode('utf-8')[i]
            cur += len(self.USVCHEADER)

            # Copy checksum @4
            for i in range(0, 4):
                finalUSC[4 + i] = ((checkSum >> i * 8) & 0xFF)

            # Copy length @8
            for i in range(0, 4):
                finalUSC[8 + i] = (int(len(binData) >> i * 8) & 0xFF)
                print("Bin Length byte: {:d}".format(finalUSC[8 + i] & 0xFF))
            print("Bin Length: {:d}".format(len(binData)))

            # Copy short title @32
            for i in range(0, min(len(shortTitle), 32)):
                finalUSC[32 + i] = shortTitle.encode('utf-8')[i]

            # Copy long titles
            for n in range(0, len(longTitle)):
                for i in range(0, min(len(longTitle[n]), 32)):
                    finalUSC[64 + n * 32 + i] = longTitle[n].encode('utf-8')[i]

            # Copy description
            for n in range(0, len(description)):
                for i in range(0, min(len(description[n]), 32)):
                    finalUSC[64 + len(longTitle) * 32 + n * 32 + i] = description[n].encode('utf-8')[i]

            # Copy authors
            for n in range(0, len(authors)):
                for i in range(0, min(len(authors[n]), 32)):
                    finalUSC[64 + (len(longTitle) + len(description)) * 32 + n * 32 + i] = authors[n].encode('utf-8')[i]

            # Copy date
            for i in range(0, min(len(date), 32)):
                finalUSC[64 + (len(longTitle) + len(description) + len(authors)) * 32 + i] = date.encode('utf-8')[i]

            # Copy version
            for i in range(0, min(len(version), 32)):
                finalUSC[64 + (len(longTitle) + len(description) + len(authors)) * 32 + 32 + i] = version.encode('utf-8')[i]

            # Copy image data @512
            for i in range(0, len(imgData)):
                finalUSC[512 + i] = imgData[i]

            # Copy bin data @512 + 512 *((PREVIEW_WIDTH * PREVIEW_HEIGHT + 511) / 512)
            for i in range(0, len(binData)):
                finalUSC[int(512 + 512 * math.floor((self.PREVIEW_WIDTH * self.PREVIEW_HEIGHT + 511) / 512) + i)] = binData[i]

            try:
                fos = open(outputFilePath, mode="wb")
                finalUSCBytes = bytes(finalUSC)
                fos.write(finalUSCBytes)
                print("Done! Bye bye!")
            except IOError as err:
                print("Cannot write to the specified output file \"{}\".".format(outputFilePath))

        if error == 0:
            return True
        else:
            return False

class PackagerCLI:

    def __init__(self):
        # No input, prompt user
        if len(sys.argv) < 2:
            print("No arguments given. Run with -h for a list of options.")
            raise SystemExit

        # Help message
        elif '-h' in sys.argv[1:] or '--help' in sys.argv[1:]:
            print("Compiled .bin file, meta .txt file, and image.png must be provided to package into .usc file.")
            print("Specify these files with the following options:")
            print("\t-b \"*.bin\" (defaults to ./binary.bin)")
            print("\t-m \"*.txt\" (defaults to ./meta.txt, see https://next-hack.com/index.php/2021/05/02/usvc-tutorial-8-how-to-run-usvc-games-from-sd-card/ for details)")
            print("\t-i \"*.png\" (defaults to ./image.png, use dimensions 96x72)")
            print("\t-o \"*.usc\" (defaults to game.usc)")
            print("\t-d \"./dir/\" (set a the working directory for all of these files, useful if keeping the default file names)")
            raise SystemExit

        # Version
        elif '-v' in sys.argv[1:] or '--version' in sys.argv[1:]:
            print("uSVC USC Packager - Version 0.11")
            raise SystemExit

        binFilePath = "binary.bin"
        metaFilePath = "meta.txt"
        imageFilePath = "image.png"
        outputFilePath = "game.usc"

        for i in range(1, len(sys.argv)):
            if sys.argv[i] == '-b':
                binFilePath = sys.argv[i + 1]
            elif sys.argv[i] == '-m':
                metaFilePath = sys.argv[i + 1]
            elif sys.argv[i] == '-i':
                imageFilePath = sys.argv[i + 1]
            elif sys.argv[i] == '-o':
                outputFilePath = sys.argv[i + 1]
            elif sys.argv[i] == '-d':
                slash = "/"
                if sys.argv[i + 1].endswith("/"):
                    slash = ""
                binFilePath = sys.argv[i + 1] + slash + binFilePath
                metaFilePath = sys.argv[i + 1] + slash + metaFilePath
                imageFilePath = sys.argv[i + 1] + slash + imageFilePath
                outputFilePath = sys.argv[i + 1] + slash + outputFilePath

            # Skip file path index
            i = i + 1

        if not binFilePath or not metaFilePath or not imageFilePath or not outputFilePath or not path.exists(binFilePath) or not path.exists(metaFilePath) or not path.exists(imageFilePath):
            print("Invalid file paths provided.")
            raise SystemExit

        packager = Packager()
        packager.createPackage(binFilePath, metaFilePath, imageFilePath, outputFilePath)

if __name__ == "__main__":
    PackagerCLI()
