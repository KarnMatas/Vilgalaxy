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
    newimg = frame[40:-86, 40:-55] # พอมีไฟแล้วมาแก้ cropsize
    kernel  = np.ones((3,3),np.uint8)/ 10
    average = cv2.filter2D(newimg, -1, kernel)
    edge = cv2.Canny(average, 10, 71) 
    return edge
def adjustment_markpath(frame):
    kernel = np.ones((2, 2), np.uint8) / 10
    kernelc = np.ones((3, 3), np.uint8) / 10
    opening = cv2.morphologyEx(frame, cv2.MORPH_CLOSE, kernelc)
    dirate1 = cv2.dilate(opening, kernelc, iterations= 31) #31   8
    erode1 = cv2.erode(dirate1, kernelc, iterations= 28) #28    28
    return erode1
def adjustment_chessboard(frame):
    # kernel = np.ones((2, 2), np.uint8) / 10
    kernelc = np.ones((3, 3), np.uint8) / 10
    opening = cv2.morphologyEx(frame, cv2.MORPH_CLOSE, kernelc)
    dirate1 = cv2.dilate(opening, kernelc, iterations= 8) #31   8
    erode1 = cv2.erode(dirate1, kernelc, iterations= 28) #28    28
    return erode1 
pathcontours=[]
thinedpath=[]
markercontours=[]
def PathFinder(frame,tune1,tune2):
    keepedge = edgedetect(frame)
    adjustimg_markpath = adjustment_markpath(keepedge)
    adjustimg_chessboard = adjustment_chessboard(keepedge)
    contours, hierarchy = cv2.findContours(adjustimg_markpath, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    for path in range(len(contours)):
        if (cv2.contourArea(contours[path]) > 25000 and cv2.contourArea(contours[path]) < 50000) :
            pathcontours.append(np.zeros(frame.shape, np.uint8))
            cv2.drawContours(pathcontours[len(pathcontours)-1],contours,path,(255,255,255),-1)
          
        if (cv2.contourArea(contours[path]) > 15000 and cv2.contourArea(contours[path]) < 25000) :
            markercontours.append(np.zeros(frame.shape, np.uint8))
            cv2.drawContours(markercontours[len(markercontours)-1],contours,path,(255,255,255),-1)
           
    # skeletonize
    # print(pathcontours[0])
    # cv2.imshow('thinpath',pathcontours[0])
    # cv2.waitKey(0)
    for path in range(len(pathcontours)):
        print(type(pathcontours[path]))
        gray = cv2.cvtColor(pathcontours[path], cv2.COLOR_BGR2GRAY)
        thinedpath = cv2.ximgproc.thinning(gray)
        cv2.imshow('thinpath',thinedpath)
        cv2.waitKey(0)
    return adjustimg_markpath

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
    cv2.waitKey(100)