"""
Package: CompressPNG
Module:  CompressPNG
Purpose: Provides a PNG Compress keyword wrapper for the RobotFramework screenshot
         
"""
__author__  = "Xia Clark <joehisaishi1943@gmail.com>"
__version__ = "1.0.1"
#
# Import the libraries we need
#
try :
    from PIL import Image
except :
    ImageGrab = None
from os import listdir
from os.path import isfile, join

#
#-------------------------------------------------------------------------------
#
class ZIPPNG(Object):
    def __init__(self):
        passs

    def isPNG(self, filePath):
        if isfile(filePath):
            if '.PNG' in filePath or '.png' in filePath:
                return True
    else:
        return False

    def compressPNG(self, mypath, colorArea=256):
        onlyfiles = [f for f in listdir(mypath) if self.isPNG(join(mypath, f))]
        print(onlyfiles)
        for pic in onlyfiles:
            im: Image.Image = Image.open(pic)
            im = im.quantize(colors=colorArea)
            im.save(pic, optimize=True)
