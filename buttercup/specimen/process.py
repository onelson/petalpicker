#! /usr/local/bin/python2.6
LOW = 90.0
HIGH = 700.0
APERATURE = 3

def DoCanny(infile, outfile, lowThresh=LOW, highThresh=HIGH, aperature=APERATURE):
    import cv
    from cv import *
    from PIL import Image, ImageOps

    lowThresh = float(lowThresh)
    highThresh = float(highThresh)
    aperature = int(aperature)
    pi = ImageOps.posterize(ImageOps.grayscale(Image.open(infile)), 5)
    cv_img = cv.CreateImageHeader(pi.size, IPL_DEPTH_8U, 1)
    cv.SetData(cv_img, pi.tostring(), pi.size[0])
    out = cv.CreateImage(cv.GetSize(cv_img), IPL_DEPTH_8U, 1)
    cv.Canny(cv_img, out, lowThresh, highThresh, aperature)
    pi = Image.fromstring("L", cv.GetSize(out), out.tostring())
    pi.save(outfile)


if '__main__' == __name__:
    import sys
    sys.path.append('/home/onelson/lib/python2.6/site-packages')
    args = sys.argv[1:]
    DoCanny(*args)
    sys.exit(0)