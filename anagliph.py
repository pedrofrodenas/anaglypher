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


def ConvertImageto3D(image):
    
    shapes = cv2.resize(image, (0,0), fx=0.4, fy=0.4)
    
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
    
    
    x, y = utils.hough_lines_coords(indicies, rhos, thetas)
    
    coefficients = utils.get_coefficients(x,y)
    
    # Get the intersection points
    CutPoints = utils.get_intersection(coefficients, M, N)
    
    
    # Plot the intersection points in the image
    fig, ax = plt.subplots()
    ax.imshow(shapes)

    for p in CutPoints:
    
        ax.plot(p[1],p[0], '+', linewidth=5, color='firebrick')
        
        
    # Selection of intersection point that is closer to everyone else
    VanishP = utils.less_distancePoint(CutPoints)
    
    
    # Plot intersection point in blue
    ax.plot(VanishP[1],VanishP[0], '+', linewidth=7, color='blue')
    
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

Image3D = ConvertImageto3D(shape)

plt.imshow(Image3D)

cv2.imwrite('imgresult.jpg',Image3D)
    
    
    
    
    
    
    
        

