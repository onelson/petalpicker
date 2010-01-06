LOW = 90.0
HIGH = 100.0
APERATURE = 3
import cv
from cv import *
from PIL import Image, ImageOps

def DoCanny(infile, outfile, lowThresh=LOW, highThresh=HIGH, aperature=APERATURE):
    pi = ImageOps.posterize(ImageOps.grayscale(Image.open(infile)), 6)
    pi.thumbnail((1024,1024))
    cv_img = cv.CreateImageHeader(pi.size, IPL_DEPTH_8U, 1)
    cv.SetData(cv_img, pi.tostring(), pi.size[0])
    out = cv.CreateImage(cv.GetSize(cv_img), IPL_DEPTH_8U, 1)
    cv.Canny(cv_img, out, lowThresh, highThresh, aperature)
    pi = Image.fromstring("L", cv.GetSize(out), out.tostring())
    pi.save(outfile)

def handle_uploaded_file(f, dest):
    dest_fh = open(dest,'wb+')
    for chunk in f.chunks():
        dest_fh.write(chunk)
    dest_fh.close()