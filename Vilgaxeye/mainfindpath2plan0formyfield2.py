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
    edge = cv2.Canny(average, 6, 98)  # 10 71  # ส่องไฟ 6 98
    return edge
def adjustment_markpath(frame):
    # kernel = np.ones((2, 2), np.uint8) / 10
    kernelc = np.ones((3, 3), np.uint8) / 10
    opening = cv2.morphologyEx(frame, cv2.MORPH_CLOSE, kernelc)
    dirate1 = cv2.dilate(opening, kernelc, iterations= 20) #31   มีไฟ 10
    erode1 = cv2.erode(dirate1, kernelc, iterations= 15) #28         5 , 7
    # cv2.imshow('test',erode1)
    return erode1
def adjustment_chessboard(frame):
    # kernel = np.ones((2, 2), np.uint8) / 10
    kernelc = np.ones((3, 3), np.uint8) / 10
    opening = cv2.morphologyEx(frame, cv2.MORPH_CLOSE, kernelc)
    dirate1 = cv2.dilate(opening, kernelc, iterations= 9) # 8  มีไฟ 9
    erode1 = cv2.erode(dirate1, kernelc, iterations= 25) # 28      25
    return erode1  
def findendp(frame):
    pix = np.copy(frame)
    for p in range(pix.shape[0]):
        for q in range(pix.shape[1]):
            if (pix[p][q] != 0):
                pix[p][q] = 1
    fakernelme = np.array([[1,1,1],
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
cornerpoints_skel = []
end_skel=[]
sortpoint=[]
anglespath=[]
world_position=[]
rf_list=[]
def spreadline(endpoints,thispath,picgrey):
    for i in range(len(centermarkers)):  #endpoint สั่งสลับ [x,y] เป็น [y,x]
        for j in range(len(endpoints)):  # ep x , ep y
            length = math.sqrt(pow((endpoints[j][1]-centermarkers[i][0]),2) + pow((endpoints[j][0]-centermarkers[i][1]),2))
            print('dolength=',length)
            if length <= 155.00:
                # print(length)
                markcolor = picgrey[endpoints[j][0],endpoints[j][1]]
                cv2.circle(picgrey, (endpoints[j][1],endpoints[j][0]), 7, int(markcolor), -1)
                # print('mark1=',markcolor)
                cv2.line(thispath, (centermarkers[i][0],centermarkers[i][1]), (endpoints[j][1],endpoints[j][0]), (255,255,255), 1)
                cv2.line(picgrey, (centermarkers[i][0],centermarkers[i][1]), (endpoints[j][1],endpoints[j][0]), int(markcolor), 10)
    for i in range(len(centerfinish)):  #endpoint สั่งสลับ [xcc,y] เป็น [y,x]
        for j in range(len(endpoints)):  # ep x , ep y
            length = math.sqrt(pow((endpoints[j][1]-centerfinish[i][0]),2) + pow((endpoints[j][0]-centerfinish[i][1]),2))
            # print('dolength2=',length)
            if length <= 155.00:
                # print(length)
                markcolor2 = picgrey[endpoints[j][0],endpoints[j][1]]
                cv2.circle(picgrey, (endpoints[j][1],endpoints[j][0]), 7, int(markcolor2), -1)
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
        Z.append(map(rawZ[k], minpix[order], maxpix[order], 20.0, 10.0)) # สลับ 10  20
    # print(rawZ)  
    # print(Z)
    rawZ = []
def convert_coordinate(lstpixel):
    yworld = (lstpixel[0] / 520) * 370
    xworld = (lstpixel[1] / 520) * 370
    yworld = (yworld - 370) * (-1)
    xworld = (xworld - 370) * (-1)
    return [xworld,yworld]
def PathFinder(frame,tune1,tune2):
    global cornerpoints_skel
    clone = frame.copy()[40:-40, 40:-40]
    # cv2.imshow("120",clone)
    # return clone
    imgGrey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    newimg = imgGrey[40:-40, 40:-40]  #40:-86, 40:-55
    newgrey = newimg.copy()
    denoiseimg = cv2.fastNlMeansDenoising(newgrey, None, 10, 7, 21)
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
            cv2.imshow('thinpath',pathcontours[0])
            cv2.waitKey(0)
        elif (cv2.contourArea(contours[path]) > 10000 and cv2.contourArea(contours[path]) < 25000) :
           # compute the center of the contour
            M = cv2.moments(contours[path])
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            markercontours.append(np.zeros(keepedge.shape, np.uint8))
            cv2.drawContours(markercontours[len(markercontours)-1],contours,path,(255,255,255),-1)
            # cv2.circle(markercontours[len(markercontours)-1], (cX, cY), 7, (0, 0, 255), -1)
            print(len(markercontours))
            cv2.waitKey(0)
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
        cv2.imshow('circle',thinedpath[0])
        cv2.waitKey(0)
    # gradientpath = cv2.bitwise_and(,)
    ##################################  ต้องมาทำเป็นสำหรับหลาย path [0] เป็น [i]
    spreadline(endpoints,thinedpath[path],newimg) # endp ,รูปที่ thined, รูปดั้งเดิมสีเทา
    fullskel = cv2.bitwise_and(pathcontours[0],thinedpath[0])
    # minus = cv2.addWeighted(fullskel,-1,thinedpath[0],1,0)
    endpoints2= findendp(fullskel) # หา จุดปลายใหม่ของ เส้นที่ ตเิมความยาวั้ง คอนทัวทั้งหมดแล้ว
    spreadline(endpoints2,fullskel,denoiseimg)
    contours2, hierarchy2 = cv2.findContours(fullskel, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    # print(len(contours2))
    epsilon = 0.05*cv2.arcLength(contours2[0],True)
    approx = cv2.approxPolyDP(contours2[0],epsilon,True)
    approximg = np.zeros(keepedge.shape, np.uint8)
    cv2.drawContours(approximg,approx,-1,(255,255,255),3)

    for ap in range(len(approx)):
        if list(approx[ap][0]) not in cornerpoints_skel:
            cornerpoints_skel.append(list(approx[ap][0]))
    for n in range(len(endpoints2)):
        end_skel.append(list(endpoints2[n]))
    # ปรับ พิกัดของ endpoints
    for e in end_skel:
        e.reverse()
    for n in range(len(end_skel)):
        if list(end_skel[n]) not in cornerpoints_skel:
            cornerpoints_skel.append(list(end_skel[n]))
    print("corner=",cornerpoints_skel)
    cv2.imshow("approximg",approximg)
    pcolor = 10
    for p in range(len(cornerpoints_skel)):
        cv2.circle(clone, (cornerpoints_skel[p][0],cornerpoints_skel[p][1]), 7, (255-(3*pcolor),255-(2*pcolor),255-(pcolor)), -1)
        pcolor+=20
    cv2.circle(clone, (422,100), 7, (0,255,0), -1)
    ##################### sort points in line ##############################################
    startpoint = centermarkers[0]
    print("start",startpoint)
    sortpoint.append(startpoint)
    # print(contours2[0][0])
    count = 0
    for p in range(len(contours2[0])):
        for q in range(len(cornerpoints_skel)):
            if count == 0:
                if list(contours2[0][p][0]) == sortpoint[0] :
                    count = 1 
            if count == 1:
                if list(contours2[0][p][0]) == cornerpoints_skel[q] :
                    # print(list(contours2[0][p][0]),cornerpoints_sskel[q])
                    if  cornerpoints_skel[q] not in sortpoint:
                        sortpoint.append(cornerpoints_skel[q])
                        print(cornerpoints_skel[q])
                    if len(sortpoint) == len(cornerpoints_skel):
                        break
    for p in range(len(contours2[0])):
        for q in range(len(cornerpoints_skel)):
            if list(contours2[0][p][0]) == cornerpoints_skel[q] :
                if  cornerpoints_skel[q] not in sortpoint:
                    sortpoint.append(cornerpoints_skel[q])
                    print(cornerpoints_skel[q])
                if len(sortpoint) == len(cornerpoints_skel):
                    break
    print("sort=",sortpoint)
    qcolor = 10
    clone2 = frame.copy()[40:-40, 40:-40]
    for p in range(len(sortpoint)):
        cv2.circle(clone2, (sortpoint[p][0],sortpoint[p][1]), 7, (255-(3*qcolor),255-(2*qcolor),255-(qcolor)), -1)
        qcolor+=20
    for poi in range(len(sortpoint)-1):
        cv2.line(clone2, (sortpoint[poi][0],sortpoint[poi][1]), (sortpoint[poi+1][0],sortpoint[poi+1][1]), (255,255,255), 1)
    cv2.circle(clone2, (sortpoint[3][0],sortpoint[3][1]), 7, (0,255,0), -1)
    ########### sortpoint เป็น list ของ เส้นทางที่เรียงจุดกันแล้ว
    ##########################  หามุม ##############################
    for p in range(len(sortpoint)-1):
        ang = math.degrees(math.atan2(sortpoint[p+1][1]-sortpoint[p][1],sortpoint[p+1][0]-sortpoint[p][0]))
        if ang < 0 :
            ang += 360
        # ang+=90
        print('p',sortpoint[p])
        print('p+1',sortpoint[p+1])
        print('now-ang= ',ang)
        anglespath.append(ang)
    ######################### เปลี่ยน coordinate ###################
    for p in range(len(sortpoint)):
        world_position.append(convert_coordinate(sortpoint[p]))
    print("world_position",world_position)
    for p in range(len(world_position)-1):
        normy = math.sqrt(math.pow((world_position[p+1][1]-world_position[p][1]),2)+math.pow((world_position[p+1][0]-world_position[p][0]),2))
        rf_list.append(normy)
    print(rf_list)
    print(newimg.shape)
    ################  plot 3d  ######################
    plotmypath(fullskel,denoiseimg,0)
    cv2.imshow('grey',newimg)
    cv2.imshow('denosie',denoiseimg)
    cv2.imshow('point',clone)
    cv2.imshow('point2',clone2)
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
    # return adjustimg_chessboard

######################################## main ########################################################
img = cv2.imread('fieldimages/myfield.png', cv2.IMREAD_COLOR)
# img = cv2.imread('fieldimages/myfieldgogo.png', cv2.IMREAD_COLOR)
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
# x = img.copy()
# func = PathFinder(x,tune1,tune2)