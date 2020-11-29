import cv2
import numpy as np
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
from matplotlib import pyplot as plt

cropsize = 40
def resize(frame,cropsize):
    oldframe = frame[cropsize:-cropsize, cropsize:-cropsize]
    return oldframe
def edgedetect(frame):
    imgGrey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    newimg = resize(imgGrey,cropsize) # crop image frame
    # newimg = imgGrey[cropsize:-cropsize, cropsize:-cropsize]
    kernel  = np.ones((3,3),np.uint8)/10
    average = cv2.filter2D(newimg, -1, kernel)
    edge = cv2.Canny(average, 8, 69) #23 85
    return edge
def adjustment(frame):
    kernel = np.ones((3, 3), np.uint8) / 10
    dirate1 = cv2.dilate(frame, kernel, iterations= 16)
    erode1 = cv2.erode(dirate1, kernel, iterations= 15)
    return erode1

def PathFinder(frame,tune1,tune2):
    keepedge = edgedetect(frame)
    adjustimg = adjustment(keepedge)
    
    return adjustimg

img = cv2.imread('fieldimages/myfield.png', cv2.IMREAD_COLOR)
cv2.namedWindow('tuner')
def nothing(x):
    pass
# create min
cv2.createTrackbar('min','tuner',10,200,nothing)
# create trackbars for max
cv2.createTrackbar('max','tuner',10,200,nothing)
# create tratrackbars for erosion contours
# cv2.createTrackbar('erodeCon','tuner',1,10,nothing)

while(1):
    tune1 = cv2.getTrackbarPos('min','tuner')
    tune2 = cv2.getTrackbarPos('max','tuner')
    x = img.copy()
    func = PathFinder(x,tune1,tune2)
    cv2.imshow('tuner',func)
    # cv2.imwrite('fieldimages/adjustfield.png', func) 
    cv2.waitKey(10)