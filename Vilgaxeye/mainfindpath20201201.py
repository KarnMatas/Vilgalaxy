import cv2
import math  
import imutils
import numpy as np
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
from matplotlib import pyplot as plt

# from CardDetect import *

# cropsize = 40
# def resize(frame,cropsize):
#     oldframe = frame[cropsize:-cropsize, cropsize:-cropsize]
#     return oldframe
def map(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
def edgedetect(frame):
    # imgGrey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # newimg = frame[40:-86, 40:-55] # พอมีไฟแล้วมาแก้ cropsize
    kernel  = np.ones((3,3),np.uint8)/ 10
    average = cv2.filter2D(frame, -1, kernel)
    edge = cv2.Canny(average, 10, 71)  # 10 71
    return edge
def adjustment_markpath(frame):
    kernel = np.ones((2, 2), np.uint8) / 10
    kernelc = np.ones((3, 3), np.uint8) / 10
    opening = cv2.morphologyEx(frame, cv2.MORPH_CLOSE, kernelc)
    dirate1 = cv2.dilate(opening, kernelc, iterations= 31) #31   
    erode1 = cv2.erode(dirate1, kernelc, iterations= 28) #28    
    cv2.imshow('test',erode1)
    return erode1
def adjustment_chessboard(frame):
    # kernel = np.ones((2, 2), np.uint8) / 10
    kernelc = np.ones((3, 3), np.uint8) / 10
    opening = cv2.morphologyEx(frame, cv2.MORPH_CLOSE, kernelc)
    dirate1 = cv2.dilate(opening, kernelc, iterations= 8) #31   8
    erode1 = cv2.erode(dirate1, kernelc, iterations= 28) #28    28
    return erode1 
def findendp(frame):
    pix = np.copy(frame)
    for p in range(pix.shape[0]):
        for q in range(pix.shape[1]):
            if (pix[p][q] != 0):
                pix[p][q] = 1
    fakernelme = np.array([[1,1,1],แ
                           [1,10,1],
                           [1,1,1]])
    filterme = cv2.filter2D(pix,-1,fakernelme)
    return np.argwhere(filterme == 11)

pathcontours=[]
thinedpath=[]
markercontours=[]
centermarkers=[] # ใช้  [x,y] ได้เลย
finishcontours=[]
centerfinish=[]
X = []
Y = []
Z = []
minpix=[]
maxpix=[]
valuepic=[]
rawZ = []
def spreadline(endpoints,thispath,picgrey):
    for i in range(len(centermarkers)):  #endpoint สั่งสลับ [x,y] เป็น [y,x]
        for j in range(len(endpoints)):  # ep x , ep y
            length = math.sqrt(pow((endpoints[j][1]-centermarkers[i][0]),2) + pow((endpoints[j][0]-centermarkers[i][1]),2))
            print('dolength=',length)
            if length <= 155.00:
                # print(length)
                # cv2.circle(picgrey, (endpoints[0][1],endpoints[0][0]), 7, (0, 0, 255), -1)
                markcolor = picgrey[endpoints[j][0],endpoints[j][1]]
                # print('mark1=',markcolor)
                cv2.line(thispath, (centermarkers[i][0],centermarkers[i][1]), (endpoints[j][1],endpoints[j][0]), (255,255,255), 1)
                cv2.line(picgrey, (centermarkers[i][0],centermarkers[i][1]), (endpoints[j][1],endpoints[j][0]), int(markcolor), 10)
    for i in range(len(centerfinish)):  #endpoint สั่งสลับ [xcc,y] เป็น [y,x]
        for j in range(len(endpoints)):  # ep x , ep y
            length = math.sqrt(pow((endpoints[j][1]-centerfinish[i][0]),2) + pow((endpoints[j][0]-centerfinish[i][1]),2))
            # print('dolength2=',length)
            if length <= 155.00:
                # print(length)
                # cv2.circle(picgrey, (endpoints[0][1],endpoints[0][0]), 7, (0, 255, 0), -1)
                markcolor2 = picgrey[endpoints[j][0],endpoints[j][1]]
                # print('mark2=',markcolor2)
                cv2.line(thispath, (centerfinish[i][0],centerfinish[i][1]), (endpoints[j][1],endpoints[j][0]), (255,255,255), 1)
                cv2.line(picgrey, (centerfinish[i][0],centerfinish[i][1]), (endpoints[j][1],endpoints[j][0]), int(markcolor2), 10)
                
def plotmypath(frame,picgrey,order): # picgrey = newimg
    global rawZ,valuepic,temp
    temp = np.argwhere(frame == 255)
    x,y = temp.T
    # print(len(temp))
    # print("x=",len(x))
    for j in range(len(temp)):
        valuepic.append(picgrey[x[j], y[j]])
        # X.append(j[1])
        # Y.append(j[0])
        rawZ.append(picgrey[x[j], y[j]])
    # print(len(valuepic))
    maxpix.append(max(valuepic))
    minpix.append(min(valuepic))
    valuepic = []
    # print(maxpix)
    for k in range(len(rawZ)):
        # if (maxpix[i] - minpix[i]) > 10.0:
        Z.append(map(rawZ[k], minpix[order], maxpix[order], 10.0, 20.0)) # สลับ 10  20
    # print(rawZ)  
    # print(Z)
    rawZ = []

def PathFinder(frame,tune1,tune2):
    imgGrey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    newimg = imgGrey[40:-86, 40:-55]
    cv2.imshow('raw',newimg)
    keepedge = edgedetect(newimg)
    adjustimg_markpath = adjustment_markpath(keepedge)
    adjustimg_chessboard = adjustment_chessboard(keepedge)
    contours, hierarchy = cv2.findContours(adjustimg_markpath, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    contours1, hierarchy1 = cv2.findContours(adjustimg_chessboard, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
 
    for path in range(len(contours)):
        look = np.zeros(keepedge.shape, np.uint8)
        cv2.drawContours(look,contours,path,(255,255,255),-1)
        cv2.imshow('cnt',look)
        cv2.waitKey(0)
        if (cv2.contourArea(contours[path]) > 25000 and cv2.contourArea(contours[path]) < 50000) :
            pathcontours.append(np.zeros(keepedge.shape, np.uint8))
            cv2.drawContours(pathcontours[len(pathcontours)-1],contours,path,(255,255,255),-1)
            # cv2.imshow('thinpath',markercontours[0])
            # cv2.waitKey(0)
        if (cv2.contourArea(contours[path]) > 15000 and cv2.contourArea(contours[path]) < 25000) :
           # compute the center of the contour
            M = cv2.moments(contours[path])
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            markercontours.append(np.zeros(keepedge.shape, np.uint8))
            cv2.drawContours(markercontours[len(markercontours)-1],contours,path,(255,255,255),-1)
            # cv2.circle(markercontours[len(markercontours)-1], (cX, cY), 7, (0, 0, 255), -1)
            centermarkers.append([cX, cY])
    Mcb = cv2.moments(contours1[0])
    cXcb = int(Mcb["m10"] / Mcb["m00"])
    cYcb = int(Mcb["m01"] / Mcb["m00"])
    finishcontours.append(np.zeros(keepedge.shape, np.uint8))
    cv2.drawContours(finishcontours[0],contours1,-1,(255,255,255),-1)
    # cv2.circle(finishcontours[0], (cXcb, cYcb), 7, (0, 0, 255), -1)
    centerfinish.append([cXcb,cYcb])
    cv2.imshow('finishpls',finishcontours[0])
    cv2.imshow('marker',markercontours[0])
    cv2.waitKey(0)

    for path in range(len(pathcontours)):
        # gray = cv2.cvtColor(pathcontours[path], cv2.COLOR_BGR2GRAY)
        thined = cv2.ximgproc.thinning(pathcontours[path])
        thinedpath.append(thined)
        endpoints = findendp(thined)
        # cv2.circle(thinedpath[0], (endpoints[0][1], endpoints[0][0]), 7, (255, 0, 0), -1)
        # cv2.circle(thinedpath[0], (endpoints[1][1], endpoints[1][0]), 7, (255, 0, 0), -1)
        cv2.imshow('circle',thinedpath[0])
    #     print(endpoints)
    #     cv2.imshow('thinpath',thined)
        cv2.waitKey(0)
        spreadline(endpoints,thinedpath[path],newimg) # endp ,รูปที่ thined, รูปดั้งเดิมสีเทา
        # print("value=",newimg[endpoints[1][1],endpoints[1][0]])
    # cv2.circle(thinedpath[0], (centermarkers[0][0], centermarkers[0][1]), 7, (255, 0, 0), -1)
    # cv2.circle(thinedpath[0], (centerfinish[0][0], centerfinish[0][1]), 7, (255, 0, 0), -1)
    cv2.imshow('enlarge',thinedpath[0])
    # for path in range(len(thinedpath)):
    #     cv2.imshow('enlarge',thinedpath[path])
    #     cv2.waitKey(0)
    ################  plot 3d ######################
    plotmypath(thinedpath[0],newimg,0)
    # tp = np.argwhere(thinedpath[0] == 255)
    # print(tp)
    # print(thinedpath[0])
    # num = 0
    # for a in range(len(thinedpath[0])):
    #     for b in range(len(thinedpath[0][a])):
    #         if thinedpath[0][a][b] > 200:
    #             print( thinedpath[0][a][b])
    cv2.imshow('grey',newimg)
    fig = plt.figure()
    ax = plt.axes(projection="3d")
    x, y = temp.T
    # ax.plot3D(X, Y, Z, 'gray')
    ax.scatter3D(x,y, Z, c=Z, cmap='hsv')
    ax.set_xlabel('X Label')
    ax.set_ylabel('Y Label')
    ax.set_zlabel('Z Label')
    # x, y = temp.T
    # plt.scatter(x,y)
    plt.show()
    cv2.waitKey(0)
    return adjustimg_markpath

######################################## main ########################################################
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