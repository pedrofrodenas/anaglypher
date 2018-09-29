import cv2
import anagliph
import string
from random import choices

# read 2D-Image input
shape = cv2.imread('images/carretera.jpg')

# Scale input image for less time computation
Image3D = anagliph.ConvertImageto3D(shape, xscale=0.3, yscale=0.3,
                                    cannymin=100, cannymax=200,
                                    nlines=4,threshold=0.7, nhood_size=80)

# Random output image name
name = ''.join(choices(string.ascii_uppercase + string.digits, k=5))

# Save 3D-Anaglyph Image
cv2.imwrite('results/{0}.jpg'.format(name),Image3D)
