import cv2
import anagliph
import string
from random import choices

# read in shapes image and convert to grayscale
shape = cv2.imread('images/carretera.jpg')


# Scale input image to less time computation
Image3D = anagliph.ConvertImageto3D(shape, xscale=0.3, yscale=0.3)


name = ''.join(choices(string.ascii_uppercase + string.digits, k=5))

cv2.imwrite('results/{0}.jpg'.format(name),Image3D)