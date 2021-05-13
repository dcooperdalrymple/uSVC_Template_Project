#!/usr/bin/env python3
# vim:fileencoding=ISO-8859-1

try:
    from PIL import Image

except ImportError as err:
    print("Could not load {} module.".format(err))
    raise SystemExit

class Utilities:

    pixelAndMask = 0b1100000011001111
    pixelOrMask = 1 << 9 # Disable SDCS
    pixelMulFactor = 1024 + 1 # Convert a uSVC encoded color byte to its signals

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
    def USVCRGBto8bit(red, green, blue):
        return ((red & 1) | ((red & 4) >> 1) | ((red & 2) << 1)  | ((blue & 1) << 3) | ((green & 1) << 4) | ((blue & 2) << 4) | ((green & 2) << 5) | ((green & 4) << 5))

    @staticmethod
    def USVCRGBtoRGB24(r, g, b):
        rgValues = [0, 32, 71, 103, 151, 184, 222, 255]
        bValues = [0, 86, 180, 255]
        return (rgValues[r & 0b0111] << 16) | (rgValues[g & 0b0111] << 8) | bValues[b & 0b0011]

    @staticmethod
    def loadImage(name):
        img = Image.open(name).convert('RGB')
        return img

    @staticmethod
    def arePicturePaletteEqual(bi1, bi2):
        # Check both png palettes?
        pal1 = bi1.getpalette() # array of color values [r, g, b, ...]
        pass
