# -*- coding: utf-8 -*-
"""
Created on Sat Aug 27 19:17:56 2016

@author: Lim
"""

import numpy as np
import cv2



#==========================
# Read video from file
#==========================

cap = cv2.VideoCapture('Walk1.mpg')

while(True):
    ret, frame = cap.read()   
    
    if ret == True:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cv2.imshow('frame',gray)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break


#==========================
# Background subtraction
#==========================


#cap = cv2.VideoCapture('walk.avi')
#
#fgbg = cv2.BackgroundSubtractorMOG()
#
#while(True):
#    ret, frame = cap.read()#    
#
#    if ret == True:
#        fgmask = fgbg.apply(frame)
#        cv2.imshow('frame',fgmask)
#        if cv2.waitKey(1) & 0xFF == ord('q'):
#            break
#    else:
#        break



#==========================
# Motion tracking by using optical flow
#==========================


#cap = cv2.VideoCapture("walk.avi")
#
#ret, frame1 = cap.read()
#prvs = cv2.cvtColor(frame1,cv2.COLOR_BGR2GRAY)
#hsv = np.zeros_like(frame1)
#hsv[...,1] = 255
#
#while(True):
#    ret, frame2 = cap.read()
#    
#    if ret == True:
#        next = cv2.cvtColor(frame2,cv2.COLOR_BGR2GRAY)
#
#        flow = cv2.calcOpticalFlowFarneback(prvs,next, 0.5, 3, 15, 3, 5, 1.2, 0)
#
#        mag, ang = cv2.cartToPolar(flow[...,0], flow[...,1])
#        hsv[...,0] = ang*180/np.pi/2
#        hsv[...,2] = cv2.normalize(mag,None,0,255,cv2.NORM_MINMAX)
#        rgb = cv2.cvtColor(hsv,cv2.COLOR_HSV2BGR)
#
#        cv2.imshow('frame2',rgb)
#        k = cv2.waitKey(1) & 0xff
#        if k == ord('q'):
#            break        
#        prvs = next
#    else:
#        break



#==========================
# For further processing or release the memory
#==========================
cv2.waitKey(0)
cap.release()
cv2.destroyAllWindows()

