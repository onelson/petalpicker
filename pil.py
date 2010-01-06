from PIL import Image, ImageOps, ImageDraw, ImageChops
import logging
from cStringIO import StringIO

logging.getLogger('pil').setLevel(logging.DEBUG)

THRESHOLD = 2
RANGE = 70

def process(fh):
    orig = Image.open(fh)
    image = ImageOps.posterize(ImageOps.grayscale(orig), 5)
    (w,h) = image.size
    (min,max) = image.getextrema()
    total = w*h
##
    im = image.load()
    pix = []
#    inc = 0
    for i in range(0,w):
        for j in range(0,h):
            threshold = range(max-RANGE,max)
            try:
                if (im[i,j] in threshold
                    and (im[i-THRESHOLD,j] not in threshold 
                    or im[i+THRESHOLD,j] not in threshold
                    or im[i,j+THRESHOLD] not in threshold
                    or im[i,j-THRESHOLD] not in threshold
                    or im[i+1,j+THRESHOLD] not in threshold
                    or im[i-1,j-THRESHOLD] not in threshold)): pix.append((i,j))
            except: pass
#            inc += 1
#    im = ImageChops.duplicate(orig)
#    pa = im.load()
#    for (x,y) in pix:
#        pa[x,y] = (0,0,255)
    
    logging.info('starting distance calculations')
    unzipped = zip(*pix)
    x = list(unzipped[0])
    y = list(unzipped[1])
    x.sort()
    y.sort()
    measure = [(x[0],y[0]),
               (x[-1],y[-1])]
    logging.debug(measure)
#    draw = ImageDraw.Draw(im)
#    coords = [(x[0],y[0]),(x[-1],y[0]),(x[-1],y[-1]),(x[0],y[-1]),(x[0],y[0])]
#    draw.line(coords,width=1,fill='#0f0')
    coords = [(x[0],y[0]),(x[-1],y[-1])]
#    draw.rectangle(coords, outline='#0f0')
    
    dist_x = (x[-1] - x[0])
    dist_y = (y[-1] - y[0])
    logging.debug((dist_x,dist_y))
    if dist_y != dist_x:
        if dist_y > dist_x: 
            dif = dist_y - dist_x
            extra = divmod(dif,2)
            x[0] -= extra[0]
            x[-1] += extra[0]
            if extra[1]: x[-1] += extra[1]
        elif dist_y < dist_x:
            dif = dist_x - dist_y
            extra = divmod(dif,2)
            y[0] -= extra[0]
            y[-1] += extra[0]
            if extra[1]: y[-1] += extra[1]
    coords = [(x[0],y[0]),(x[-1],y[-1])]
    return coords
#    logging.debug(coords)
#    draw.ellipse(coords, outline='#f00')
#    combo = ImageChops.screen(orig, im)
#    im.save(fh)
#    return True
