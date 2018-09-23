#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 22 22:03:31 2018

@author: PedrofRodenas
"""

# imports
import numpy as np

def hough_lines_coords(indicies, rhos, thetas):
    
    x = []
    y = []
    
    
    for i in range(len(indicies)):
        # reverse engineer lines from rhos and thetas
        rho = rhos[indicies[i][0]]
        theta = thetas[indicies[i][1]]
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a*rho
        y0 = b*rho
        # these are then scaled so that the lines go off the edges of the image
        x1 = int(x0 + 1000*(-b))
        y1 = int(y0 + 1000*(a))
        x2 = int(x0 - 1000*(-b))
        y2 = int(y0 - 1000*(a))
        x.append([x1,x2])
        y.append([y1,y2])
        
    return np.array(x), np.array(y)


# Get the coefficients of straight line [m,n] slope-point
def get_coefficients(x,y):
    
    coeff= []
    
    for i in range(len(x)):
    
        coeff.append(np.polyfit(x[i], y[i], 1))
        
    return np.array(coeff)


# Get intersection points solving lineal equation two variables
# coeff is the list of cut point by y-axis  (n) and slope (m) 
# coeff = [[m,n],...]
# M and N are the size of image    

def get_intersection(coeff, M, N):
    
    dim = np.array([M,N])
    
    # Number of lines
    n = len(coeff)

    resul = []
    
    # Solving following system of linear equation
    # y - m1x = n1
    # y - m2x = n2
    for i in range(n-1):
    
        for j in range(i+1,n):
        
            b = [coeff[i][1],coeff[j][1]]
            a = [[1, -coeff[i][0]],[1, -coeff[j][0]]]
        
            res = np.rint(np.linalg.solve(a,b)).astype(int)
        
            # Check if intersection point is inside of image boundaries
            if np.all(res > 0) & (dim>=res).all():
        
                resul.append(res)
                
    resul = np.array(resul)
    
    # Delete points of parallel or coincident lines
    resul = np.unique(resul, axis=0)
    
    return resul



# Selection of intersection point that is closer to everyone else
# Input is the list of intersection points
def less_distancePoint(CutPoints):
    
    distances = []
    
    for i in range(len(CutPoints)):
    
        allp = np.copy(CutPoints)
    
        point = allp[i]
    
        np.delete(allp, i, 0)
    
        distance = 0
    
    for pts in allp:
        
        distance = distance + np.linalg.norm(pts - point)
        
    distances.append(distance)

    distances = np.array(distances)
    
    # Get the index of minimum value
    ind = np.argmin(distances)
    
    # Vanishing Point
    VanishP = CutPoints[ind]
    
    return VanishP



    
                
                
                
        
        
    
    
    
