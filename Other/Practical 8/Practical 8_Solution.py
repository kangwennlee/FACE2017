# -*- coding: utf-8 -*-
"""
Created on Sat Aug 27 22:06:47 2016

@author: Lim
"""
import numpy as np
import cv2


#==========================
# Exercise Q1
#==========================

img = cv2.imread('map.png')
cv2.imshow('pic1',img)


# Extract the river 
lower_river = np.array([240,185,120])
upper_river = np.array([260,205,150])
mask_river = cv2.inRange(img, lower_river, upper_river)
river = cv2.bitwise_and(img, img, mask = mask_river)
cv2.imshow("pic_river", river)


# Extract the road
lower_road = np.array([100,205,245])
upper_road = np.array([170,230,265])
mask_road = cv2.inRange(img, lower_road, upper_road)
road = cv2.bitwise_and(img, img, mask = mask_road)
cv2.imshow("pic_road", road)

# Extract the field
lower_field = np.array([179,220,204])
upper_field = np.array([199,240,224])
mask_field = cv2.inRange(img, lower_field, upper_field)
field = cv2.bitwise_and(img, img, mask = mask_field)
cv2.imshow("pic_field", field)

# Extract the building
lower_building = np.array([228,214,235])
upper_building = np.array([248,254,255])
mask_building = cv2.inRange(img, lower_building, upper_building)
building = cv2.bitwise_and(img, img, mask = mask_building)
cv2.imshow("pic_building", building)

cv2.waitKey(0)
cv2.destroyAllWindows()

#==========================
# Exercise Q2 
#==========================

#cap = cv2.VideoCapture('walk.avi')
#
#fgbg = cv2.BackgroundSubtractorMOG()
#
#fgmask_Threshold = 0.03 #apply threshold of 30% of the screen is filled with unintended object
#
#while(True):
#    ret, frame = cap.read()
#
#    fgmask = fgbg.apply(frame)
#    
##    plt.imshow(fgmask, cmap = 'gray', interpolation = 'bicubic')
##    plt.xticks([]), plt.yticks([])  # to hide tick values on X and Y axis
##    plt.show()    
#    
#    #Intrusion detection
#    if ret==True:
#        fgmask_Filter = fgmask>1
#        fgmask_Intrusion = sum(sum(fgmask_Filter))
#    
#        if float(fgmask_Intrusion)/(float(120)*float(160)) > fgmask_Threshold:
#            intrusion = 1        
#        else:
#            intrusion = 0   
#        
#        print intrusion
#        
#        cv2.imshow('frame',fgmask)
#        if cv2.waitKey(1) & 0xFF == ord('q'):
#            break   
#    else:
#        break
#        
#cv2.waitKey(0)
#cap.release() # Release the capture when everything is done
#cv2.destroyAllWindows()


#==========================
# Exercise Q3: Capture video from webcam
#==========================

#cap = cv2.VideoCapture(0)
#
#while(True):
#    # Capture frame-by-frame
#    ret, frame = cap.read()
#
#    if ret == True:
#        # Our operations on the frame come here
#        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#
#        # Display the resulting frame
#        cv2.imshow('frame',gray)
#        if cv2.waitKey(1) & 0xFF == ord('q'):
#            break
#    else:
#        break
#
#
#cv2.waitKey(0)
#cap.release() # Release the capture when everything is done
#cv2.destroyAllWindows()