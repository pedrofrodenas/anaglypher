#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 22 22:03:31 2018

@author: PedrofRodenas
"""

# imports
import numpy as np
import cv2
import matplotlib.pyplot as plt
import utils
import hough
import string
from random import choices
import matplotlib.patches as mpatches


def plot_CutPoints(img, cutP, VanishP):
    
    
    fig, ax = plt.subplots()
    ax.imshow(img)
    
    ax.axis('off')
    red_patch = mpatches.Patch(color='firebrick', label='Cut Points')
    blue_patch = mpatches.Patch(color='blue', label='Vanishing Point')
    
    for p in cutP:
    
        ax.plot(p[1],p[0], '+', linewidth=5, color='firebrick')
        
    # Plot intersection point in blue
    ax.plot(VanishP[1],VanishP[0], '+', linewidth=7, color='blue')
    ax.legend(handles=[red_patch, blue_patch])
    
    


def ConvertImageto3D(image, xscale, yscale):
    
    shapes = cv2.resize(image, (0,0), fx=xscale, fy=yscale)
    
    M, N, D = shapes.shape
    
    imagen = np.copy(shapes)
    
    shapes_grayscale = cv2.cvtColor(shapes, cv2.COLOR_RGB2GRAY)
    
    # blur image (this will help clean up noise for Canny Edge Detection)
    # see Chapter 2.0 for Guassian Blur or check OpenCV documentation
    shapes_blurred = cv2.GaussianBlur(shapes_grayscale, (5, 5), 1.5)

    # find Canny Edges and show resulting image
    canny_edges = cv2.Canny(shapes_blurred, 100, 200)
    plt.imshow(canny_edges, cmap='gray')
    plt.title("Canny Edges")

    # run hough_lines_accumulator on the shapes canny_edges image
        
    H, rhos, thetas = hough.hough_lines_acc(canny_edges)
    indicies, H = hough.hough_peaks(H, 4,threshold=0.7, nhood_size=80) # find peaks
    hough.plot_hough_acc(H) # plot hough space, brighter spots have higher votes
    hough.hough_lines_draw(shapes, indicies, rhos, thetas)
    
    
    plt.imshow(shapes)
    plt.title('Lines Detected')
    plt.axis('off')
    
    
    x, y = utils.hough_lines_coords(indicies, rhos, thetas)
    
    coefficients = utils.get_coefficients(x,y)
    
    # Get the intersection points
    CutPoints = utils.get_intersection(coefficients, M, N)
        
        
    # Selection of intersection point that is closer to everyone else
    VanishP = utils.less_distancePoint(CutPoints)
    
    # Plot cut points and vanishing point
    plot_CutPoints(shapes, CutPoints, VanishP)
    
    # Memory reservation for DephMap
    DepthMap = np.zeros((M,N))
    DepthMapL = np.zeros((M,N))
    DepthMapR = np.zeros((M,N))

    xvan = VanishP[0]
    yvan = VanishP[1]

    # DepthMap Synthesis at vertical axis
    for i in range(M):
    
        DepthMap[i,:] = (255/(M-xvan))*(i-xvan)
        
    # Convert to 0 negatives values
    DepthMap[DepthMap < 0] = 0
       
    # DepthMap Synthesis at horizontal axis
    for i in range(yvan):
    
        DepthMapL[xvan:,i] = -(255/yvan)*(i-yvan)
    
    for i in range(yvan,N):
    
        DepthMapR[xvan:,i] = (255/(N-yvan))*(i-yvan)
        
    DepthMapH = DepthMapL + DepthMapR
    
    
    # Maximum displacement of image
    Md = int(N / 95)

    # Parallax Matrix Vertical Shift
    parallax = (Md*((DepthMap/255))).astype(int)

    # Parallax Matrix Vertical Shift
    parallaxh = (Md*((DepthMapH/255))).astype(int)
    
    # Copy third channel (Red)
    imgR = imagen[:,:,2]
    
    # Image border extension
    img = cv2.copyMakeBorder(imagen,0,0,Md,Md,
                             cv2.BORDER_CONSTANT,value=0)

    pp = (parallax + parallaxh)
    
    # Channel displacement
    for i in range(M):
    
        for j in range(N):
        
            img[i,j+pp[i,j],2] = imgR[i,j]


    Image3D = img[:,Md:-Md,:]
    
    return Image3D


# read in shapes image and convert to grayscale
shape = cv2.imread('images/carretera.jpg')


# Scale input image to less time computation
Image3D = ConvertImageto3D(shape, xscale=0.3, yscale=0.3)

plt.figure()
plt.imshow(Image3D)
plt.title('Anaglyph 3D')
plt.axis('off')

name = ''.join(choices(string.ascii_uppercase + string.digits, k=5))

cv2.imwrite('results/{0}.jpg'.format(name),Image3D)
    
    
    
    
    
    
    
        

