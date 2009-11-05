from PIL import Image, ImageOps, ImageDraw, ImageChops
import logging
#import decimal 

logging.getLogger().setLevel(logging.DEBUG)

IN = 'E:/flower_small.jpg'
OUT = 'E:/OUT.jpg'
OUT2 = 'E:/OUT2.jpg'
THRESHOLD = 2
RANGE = 70
orig = Image.open(IN)
image = ImageOps.posterize(ImageOps.grayscale(orig), 5)


(w,h) = image.size
(min,max) = image.getextrema()
#logging.debug((w,h,min,max))

total = w*h

def pix_access():
    im = image.load()
    pix = []
    inc = 0
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
            inc += 1
            
#            logging.debug(decimal.Decimal(inc)/decimal.Decimal(total)*100)
    im = ImageChops.duplicate(orig)
    pa = im.load()
    for (x,y) in pix:
        pa[x,y] = (0,0,255)
    
    logging.info('starting distance calculations')
    unzipped = zip(*pix)
    x = list(unzipped[0])
    y = list(unzipped[1])
    x.sort()
    y.sort()
    measure = [(x[0],y[0]),
               (x[-1],y[-1])]
    logging.debug(measure)
    draw = ImageDraw.Draw(im)
    coords = [(x[0],y[0]),(x[-1],y[0]),(x[-1],y[-1]),(x[0],y[-1]),(x[0],y[0])]
    draw.line(coords,width=1,fill='#0f0')
#    coords = [(x[0],y[0]),(x[-1],y[-1])]
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
    logging.debug(coords)
    draw.ellipse(coords, outline='#f00')
    
        
    
#    combo = ImageChops.screen(orig, im)
    im.save(OUT)
#    
        
def to_coord(index):
    global w
    width = w
    return divmod(index,width)

def to_index(offset_x,offset_y):
    global w
    width = w
    if 0 == offset_y: return offset_x
    else: return (offset_y * width) + offset_x 

def seq_access():
    new_data = []
    for k,p in enumerate(image.getdata()):
        threshold = range(max-RANGE,max)
        try:
            coords = to_coord(k)
            if (p in threshold
                and (to_index(coords[0]-THRESHOLD, coords[1]) not in threshold 
                or to_index(coords[0]+THRESHOLD, coords[1]) not in threshold
                or to_index(coords[0], coords[1]-THRESHOLD) not in threshold
                or to_index(coords[0], coords[1]+THRESHOLD) not in threshold
                or to_index(coords[0]-THRESHOLD, coords[1]-THRESHOLD) not in threshold
                or to_index(coords[0]+THRESHOLD, coords[1]+THRESHOLD) not in threshold)): new_data.append((255,0,0))
        except Exception as err: logging.error(err)
        try: new_data[k]
        except: new_data.append((0,0,0))
#        logging.debug(decimal.Decimal(k)/decimal.Decimal(total)*100)
    temp = Image.new('RGB',(w,h))
    temp.putdata(new_data)
    temp.save(OUT)

#from timeit import Timer
#t = Timer('pix_access()', 'from __main__ import pix_access')

#t2 = Timer('seq_access()','from __main__ import seq_access')

#print t.timeit(100)
#print t2.timeit(100)

pix_access()