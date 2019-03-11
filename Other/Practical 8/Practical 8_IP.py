# -*- coding: utf-8 -*-
"""
Created on Thu Aug 18 23:45:55 2016

@author: Lim
"""

import numpy as np
import cv2


#=========================
# This example perform image resize and grayscale conversion using Lenna image.
#=========================     
img = cv2.imread('Lenna.png')
cv2.imshow('picOriLenna',img)

# Image resize
imgResize = cv2.resize(img,None,fx=1.5, fy=1.5)
cv2.imshow('picResized',imgResize)

# Gray image conversion
gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
cv2.imshow('picGray',gray_image)


#=========================
# This example perform morphological operation on Digit image
#=========================

imgDigit = cv2.imread('Digit3.png')
cv2.imshow('picOriDigit',imgDigit)

#Kernel initialization

# Erosion
kernel = np.ones((3,3),np.uint8)
erosion = cv2.erode(imgDigit,kernel,iterations = 1)
cv2.imshow('picErosion',erosion)

# Dilation
kernel = np.ones((5,5),np.uint8)
dilation = cv2.dilate(imgDigit,kernel,iterations = 1)
cv2.imshow('picDilation',dilation)

# Opening
kernel = np.ones((3,3),np.uint8)
opening = cv2.morphologyEx(imgDigit, cv2.MORPH_OPEN, kernel)
cv2.imshow('picOpening',opening)

# Closing
kernel = np.ones((5,5),np.uint8)
closing = cv2.morphologyEx(imgDigit, cv2.MORPH_CLOSE, kernel)
cv2.imshow('picClosing',closing)



#=========================
# This example perform image denoise - use different filter on cameraman image
#=========================

#Apply salt and pepper noise
imgNoise = cv2.imread("cameraman_noise.jpg")
gray_imgNoise = cv2.cvtColor(imgNoise, cv2.COLOR_BGR2GRAY)
cv2.imshow('picOriNoise',gray_imgNoise)

# Averaging filtering
blurAverage = cv2.blur(gray_imgNoise,(10,10))
cv2.imshow('picBlur',blurAverage)

# Gaussian filtering
blurGauss = cv2.GaussianBlur(gray_imgNoise,(5,5),0)
cv2.imshow('picBlurGauss',blurGauss)

# Median filtering
blurMedian = cv2.medianBlur(gray_imgNoise,5)
cv2.imshow('picBlurMedian',blurMedian)



#=========================
# This example perform Edge and corner detection using chessboard image
#=========================

filename = 'Chessboard.png'
img = cv2.imread(filename)
img = cv2.resize(img,None,fx=0.5, fy=0.5)
cv2.imshow('picOriChessboard',img)

# Edge detection using canny operator
edgesCanny = cv2.Canny(img,100,200)
cv2.imshow('picEdgeCanny',edgesCanny)


# Corner detection using Harris corner detector
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
gray = np.float32(gray)
dst = cv2.cornerHarris(gray,2,3,0.04)

dst = cv2.dilate(dst,None) #result is dilated for marking the corners, not important

img[dst>0.01*dst.max()]=[0,0,255] # Threshold for an optimal value, it may vary depending on the image.

cv2.imshow('dst',img)


# wait or user input on pressing any key then destroy the windows
cv2.waitKey(0)
cv2.destroyAllWindows()