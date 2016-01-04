from pylab import arange, plot, sin, ginput, show
from PIL import Image, ImageEnhance, ImageDraw, ImageOps, ImageFilter
from scipy.ndimage import gaussian_filter
import matplotlib.pyplot as plt, matplotlib, sys, numpy as np, math, scipy
from skimage.restoration import denoise_bilateral
from images2gif import writeGif

MASK_WIDTH, MASK_HEIGHT = 640, 480

def selectPoints(im):
    im = Image.open(im)
    plt.imshow(im)
    counter, f_points = 1, []
    print "Select a point in the image to determine focus line."
    while counter != 0:
        print counter, "clicks left"
        x = ginput(1)
        counter -= 1
        f_points.append([x[0][0], x[0][1]])
        plt.scatter(x[0][0], x[0][1])
        plt.draw()
    print "Close the pyplot window so that we can continue computation!"
    plt.show()
    return f_points

def createMiniature(im, pts, custom_mask=None, dof=40, color=1.9, contrast=1.4, offset_focus=9):
    # Cranking up the contrast and color
    edited = ImageEnhance.Contrast(ImageEnhance.Color(im).enhance(color)).enhance(contrast)
    # Determining whether we want a focal line mask or a custom mask (bells and whistles)
    if not custom_mask:
        # Creating the mask for a focal line

        # offset = int(pts[0][1] / im.size[1] * MASK_HEIGHT)
        # print offset
        # va = int(offset + 81.6)
        # focus = int(va + offset_focus * 4.8)
        # vb = int(focus + 43.2)

        offset = int(pts[0][1] / float(im.size[1]) * MASK_HEIGHT)
        #print(pts[0][1], im.size[1], MASK_HEIGHT, offset) 
        va = int(offset + 81.6)
        focus = int(va + offset_focus * 4.8)
        vb = int(focus + 43.2)

        mask, m1 = Image.new('L', (MASK_WIDTH, MASK_HEIGHT)), Image.new('L', (1, MASK_HEIGHT))
        d1 = ImageDraw.Draw(m1)
        for i in range (0, offset):
            d1.point((0, i), 255)
        for i in range (offset, va):
            d1.point((0, i), (va - i) * (255 / (va - offset)))
        for i in range (va, focus):
            d1.point((0, i), 0)
        for i in range (focus, vb):
            d1.point((0, i), 255 - (vb - i) * (255 / (vb - focus)))
        for i in range (vb, MASK_HEIGHT):
            d1.point((0, i), 255)
        mt = ImageOps.invert(ImageOps.invert(m1.resize((int(mask.size[0] * 3), mask.size[1]), Image.ANTIALIAS)).rotate(0, Image.NEAREST, 1))
        mask.convert("RGBA")
        mask.paste(mt,(-mt.size[0] / 2, -(mt.size[1] / 2 - MASK_HEIGHT / 2)))
        mask.convert("L")
        mask = mask.resize(edited.size)
    else:
        # hello from the other side
        #mask = custom_mask.convert("1")
        lol = Image.fromarray(np.uint8(gaussian_filter(np.array(custom_mask, dtype=float), sigma=[3, 3, 0])))
        mask = lol.convert("1")
        # mask = mask.point(lambda i:i*(1./256)).convert('L') #.filter(ImageFilter.SMOOTH)
        #return lol

    # Blurring the image and merging
    if custom_mask:
        im_blur = Image.fromarray(np.uint8(gaussian_filter(np.array(edited, dtype=float), sigma=[1, 1, 0])))
    else:
        im_blur = Image.fromarray(np.uint8(gaussian_filter(np.array(edited, dtype=float), sigma=[4, 4, 0])))
    edited = edited.convert("RGBA")
    edited.paste(im_blur, mask=mask)

    return edited

def createMiniatureGif(image):
    frame, n, out = Image.open(image), 0, []
    try:
        while 1:
            out.append(createMiniature(frame.copy().convert('RGBA'), [[50, 90]]))
            frame.seek(frame.tell() + 1)
    except EOFError:
        return out
    # while frame:
    #     out.append(createMiniature(frame, [[0, 100]]))
    #     try:
    #         frame.seek(n)
    #     except EOFError:
            # break;
    #     n += 1
    # return out

# Creating Normal
# if len(sys.argv) > 2:
#     x = createMiniature(Image.open(sys.argv[1]), [], custom_mask=Image.open(sys.argv[2]))
# else:
#     x = createMiniature(Image.open(sys.argv[1]), selectPoints(sys.argv[1]))

# if len(sys.argv) > 2:
#     scipy.misc.imsave('minature_output.jpg', x)
# else:
#     x.save("minature_output.jpg")
# print "Image is saved in the directory as minature_output.jpg!"

# Creating Gif
out = createMiniatureGif("m.gif")
writeGif("lol.GIF", out, duration=0.04)