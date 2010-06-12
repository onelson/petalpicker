import os, logging, sys
from opencv.cv import *
DATA_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)),'data')
IN = os.path.join(DATA_DIR,'sample.jpg')
OUT = os.path.join(DATA_DIR,'out.jpg')
LOG_FILENAME = os.path.join(DATA_DIR,'exp.log')
logging.basicConfig(name='exp',filename=LOG_FILENAME,level=logging.DEBUG)

LOW = 90.0
HIGH = 100.0
APERATURE = 3


def DoCanny(img, lowThresh=LOW, highThresh=HIGH, aperature=APERATURE):
#    gray = cvCreateImage(cvSize(cvGetSize(img).width, cvGetSize(img).height), IPL_DEPTH_8U, 1)
#    cvCvtColor(img,gray,CV_RGB2GRAY)
    
#    if (gray.nChannels != 1):
#        return False
    logging.info('creating out image')
    out = cvCreateImage(cvSize(cvGetSize(img).width, cvGetSize(img).height), IPL_DEPTH_8U, 1)
    logging.info('out image prepared')
    logging.info('running canny')
    cvCanny(img, out, lowThresh, highThresh, aperature)
    logging.info('canny complete')
    return out

def main():
    logging.info('Starting up...')
    logging.debug(IN+' -> '+OUT)
    frame = cvLoadImage(IN, CV_LOAD_IMAGE_GRAYSCALE)
    logging.debug('Got frame...')
    #cvShowImage("Example5", frame)
    logging.info('Doing Canny...')
    outCan = DoCanny(frame)
    logging.info('done.')
    #cvShowImage("Example5-Canny", outCan)
    logging.info('Saving image...')
    try:
        cvSaveImage(OUT,outCan)
    except Exception as err:
        logging.error(err)
        raise err
    logging.info('done.')
    
    sys.exit(0)
if '__main__' == __name__: main()