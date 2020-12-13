import cv2
import math  
import imutils
import numpy as np
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
# from CardDetect import *

cropsize = 35
# def resize(frame,cropsize):
#     oldframe = frame[cropsize:-cropsize, cropsize:-cropsize]
#     return oldframe
def map(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
def edgedetect(frame):
    # imgGrey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # newimg = frame[40:-86, 40:-55] # พอมีไฟแล้วมาแก้ cropsizec
    kernel  = np.ones((3,3),np.uint8)/10
    average = cv2.filter2D(frame, -1, kernel)
    edge = cv2.Canny(average, 17, 50) # 35 142
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
minpix=0
maxpix=0
maxpixlst =[]
minpixlst =[]
valuepic=[]
rawZ = []
rawZfull=[]
cornerpoints_skel = []
end_skel=[]
sortpoint=[]
sortpointZ=[] # ค่า z จะส่งออก
anglespath=[]
anglesZ=[]
world_position=[]
rf_list=[]
# rfZ_list=[]
def spreadline(endpoints,thispath,picgrey):
    print('centermarker',len(centermarkers))
    print('endpoints',len(endpoints))
    for i in range(len(centermarkers)):  #endpoint สั่งสลับ [x,y] เป็น [y,x]  len(centermarkers)
        for j in range(len(endpoints)):  # ep x , ep y     len(endpoints)
            length = math.sqrt(pow((endpoints[j][1]-centermarkers[i][0]),2) + pow((endpoints[j][0]-centermarkers[i][1]),2))
            # print('dolength=',length)
            if length <= 155.00:
                # print(length)
                markcolor = picgrey[endpoints[j][0],endpoints[j][1]]
                cv2.circle(picgrey, (endpoints[j][1],endpoints[j][0]), 7, int(markcolor), -1)
                # print('mark1=',markcolor)c
                cv2.line(thispath, (centermarkers[i][0],centermarkers[i][1]), (endpoints[j][1],endpoints[j][0]), (255,255,255), 1)
                cv2.line(picgrey, (centermarkers[i][0],centermarkers[i][1]), (endpoints[j][1],endpoints[j][0]), int(markcolor), 10)
    for i in range(len(centerfinish)):  #endpoint สั่งสลับ [xcc,y] เป็น [y,x]   len(centerfinish)
        for j in range(len(endpoints)):  # ep x , ep y     len(endpoints)
            length = math.sqrt(pow((endpoints[j][1]-centerfinish[i][0]),2) + pow((endpoints[j][0]-centerfinish[i][1]),2))
            # print('dolength2=',length)
            if length <= 155.00:
                # print(length)
                markcolor2 = picgrey[endpoints[j][0],endpoints[j][1]]
                cv2.circle(picgrey, (endpoints[j][1],endpoints[j][0]), 7, int(markcolor2), -1)
                # print('mark2=',markcolor2)
                cv2.line(thispath, (centerfinish[i][0],centerfinish[i][1]), (endpoints[j][1],endpoints[j][0]), (255,255,255), 1)
                cv2.line(picgrey, (centerfinish[i][0],centerfinish[i][1]), (endpoints[j][1],endpoints[j][0]), int(markcolor2), 10)

def getZ(frame,picgrey):
    global rawZ,temp,sortpointZ
    temp = np.argwhere(frame == 255)
    x,y = temp.T
    print(len(temp))
   
    for val in range(len(temp)):
        rawZ.append(picgrey[x[val], y[val]])
    # print('rawz',rawZ)
    maxpix= max(rawZ)
    minpix= min(rawZ)
    print('minpix',minpix)
    print('maxpix',maxpix)
    # for val in range(len(temp)):
    #     Z.append(map(val, minpix, maxpix, 20.0, 10.0))
    temp_sortpoint = []
    if len(pathcontours) > 1:
        ihave = 0
        for point in range(len(sortpoint)):
            for i in range(len(x)):
                # print([x[i],y[i]],sortpoint[point])
                # print(type(x[i]),type(sortpoint[point]))

                if [int(x[i]),int(y[i])] == [int(sortpoint[point][0]),int(sortpoint[point][1])]:
                    print("iwantsleep",[[x[i],y[i]],sortpoint[point]])
                    Zsword = picgrey[sortpoint[point][0],sortpoint[point][1]]
                    realsword = map(Zsword, minpix, maxpix, 20.0, 10.0) 
                    if realsword >= 15.00 :
                        realsword = 20.00
                    elif realsword < 15.00 :
                        realsword = 10.00
                    temp_sortpoint.append(realsword) 
                    ihave = 1
                    break
            if ihave == 0:
                temp_sortpoint.append(0)
            else:
                ihave = 0
        if len(sortpointZ) != 0:
            for num in range(len(temp_sortpoint)):
                if sortpointZ[num] == 0:
                    sortpointZ[num] = temp_sortpoint[num] 
        else:
            sortpointZ = temp_sortpoint
    elif len(pathcontours) == 1:
        for point in range(len(sortpoint)):
            Zsword = picgrey[sortpoint[point][0],sortpoint[point][1]]
            realsword = map(Zsword, minpix, maxpix, 20.0, 10.0) 
            print('realsword',realsword)
            Threshold = 11.0
            if realsword >= Threshold :  #15 default
                realsword = 20.00
            elif realsword < Threshold :
                realsword = 10.00
            temp_sortpoint.append(realsword) 
        if len(sortpointZ) != 0:
            for num in range(len(temp_sortpoint)):
                if sortpointZ[num] == 0:
                    sortpointZ[num] = temp_sortpoint[num] 
        else:
            sortpointZ = temp_sortpoint
    # while (0 in sortpointZ):
    #     print("Karn")


    # print('temp',temp)
    # for point in range(len(sortpoint)):
    #     if picgrey[sortpoint[point][0],sortpoint[point][1]] == 255 :
    #         Zsword = picgrey[sortpoint[point][0],sortpoint[point][1]]
    #         realsword = map(Zsword, minpix, maxpix, 20.0, 10.0) 
    #         if realsword >= 15.00 :
    #             realsword = 20.00
    #         elif realsword < 15.00 :
    #             realsword = 10.00
    #         sortpointZ.append(realsword)
    print('sourceped',sortpointZ)
    rawZ = []
    maxpix= 0
    minpix= 0
def plotmypath(frame,picgrey,order): # picgrey = newimg
    global rawZfull,valuepic,temp,tempfullpath
    tempfullpath = np.argwhere(frame == 255)
    xf,yf = tempfullpath.T
    # print(len(temp))
    # print("x=",len(x))
    for j in range(len(tempfullpath)):
        valuepic.append(picgrey[xf[j], yf[j]])
        # X.append(j[1])
        # Y.append(j[0])
        rawZfull.append(picgrey[xf[j], yf[j]])
    # print(len(valuepic))
    maxpixlst.append(max(valuepic))
    minpixlst.append(min(valuepic))
    valuepic = []
    # print(maxpix)
    for k in range(len(rawZfull)):
        # if (maxpix[i] - minpix[i]) > 10.0:
        Z.append(map(rawZfull[k], minpixlst[order], maxpixlst[order], 20.0, 10.0)) # สลับ 10  20
    # print(rawZ)  
    # print(Z)
    rawZfull = []

def convert_coordinate(lstpixel):
    yworld = (lstpixel[1] / 530) * 390
    xworld = (lstpixel[0] / 530) * 390
    # yworld = (yworld - 370) * (-1)
    # xworld = (xworld - 370) * (-1)
    return [xworld,yworld]


def PathFinder(frame): #,tune1,tune2
    global cornerpoints_skel
    clone = frame.copy()[cropsize:-cropsize, cropsize:-cropsize]
    imgGrey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    newimg = imgGrey[cropsize:-cropsize, cropsize:-cropsize]  #40:-86, 40:-55
    newgrey = newimg.copy()
    denoiseimg = cv2.fastNlMeansDenoising(newgrey, None, 10, 7, 21)
    cv2.imshow('raw',newimg)
    cv2.imshow('denoise',denoiseimg)
    keepedge = edgedetect(newimg)
    # return keepedge
    adjustimg_markpath = adjustment_markpath(keepedge)
    # return adjustimg_markpath
    adjustimg_chessboard = adjustment_chessboard(keepedge)
    contours, hierarchy = cv2.findContours(adjustimg_markpath, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    contours1, hierarchy1 = cv2.findContours(adjustimg_chessboard, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    
    for path in range(len(contours)):
        look = np.zeros(keepedge.shape, np.uint8)
        cv2.drawContours(look,contours,path,(255,255,255),-1)
        cv2.imshow('cnt',look)  #---++
        cv2.waitKey(0)
        # print('area',cv2.contourArea(contours[path]))
        if (cv2.contourArea(contours[path]) > 17000 and cv2.contourArea(contours[path]) < 50000 ) :
            # print('area',cv2.contourArea(contours[path]))
            pathcontours.append(np.zeros(keepedge.shape, np.uint8))
            cv2.drawContours(pathcontours[len(pathcontours)-1],contours,path,(255,255,255),-1)
            # cv2.imshow('thinpath',pathcontours[0])---++
            # print("len(path)=",len(pathcontours))
            # cv2.waitKey(0)
        elif (cv2.contourArea(contours[path]) > 10000 and cv2.contourArea(contours[path]) < 17000) :
            # print('area',cv2.contourArea(contours[path]))
           # compute the center of the contour
            M = cv2.moments(contours[path])
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            markercontours.append(np.zeros(keepedge.shape, np.uint8))
            cv2.drawContours(markercontours[len(markercontours)-1],contours,path,(255,255,255),-1)
            # cv2.circle(markercontours[len(markercontours)-1], (cX, cY), 7, (0, 0, 255), -1)
            # print("len(marker)=",len(markercontours))
            cv2.waitKey(0)
            centermarkers.append([cX, cY])
    Mcb = cv2.moments(contours1[0])
    cXcb = int(Mcb["m10"] / Mcb["m00"])
    cYcb = int(Mcb["m01"] / Mcb["m00"])
    finishcontours.append(np.zeros(keepedge.shape, np.uint8))
    cv2.drawContours(finishcontours[0],contours1,-1,(255,255,255),-1)
    # cv2.circle(finishcontours[0], (cXcb, cYcb), 7, (0, 0, 255), -1)
    centerfinish.append([cXcb,cYcb])
    cv2.imshow('finishpls',finishcontours[0])#----++
    cv2.imshow('marker',markercontours[0])#----++
    cv2.waitKey(0)

    for path in range(len(pathcontours)):
        # gray = cv2.cvtColor(pathcontours[path], cv2.COLOR_BGR2GRAY)
        thined = cv2.ximgproc.thinning(pathcontours[path])
        thinedpath.append(thined)
        endpoints = findendp(thined)
        # cv2.imshow('thined',thinedpath[path])---+++
        # cv2.waitKey(0)
    # gradientpath = cv2.bitwise_and(,)
    ##################################  ต้องมาทำเป็นสำหรับหลาย path [0] เป็น [i]
        spreadline(endpoints,thinedpath[path],newimg) # endp ,รูปที่ thined, รูปดั้งเดิมสีเทา
    endpoints2 = []
    pathlst = [] # เก็บ path ที่ ทำ skeletonize กับ ขยายเส้นแล้ว
    for path in range(len(pathcontours)):
        fullskel = cv2.bitwise_and(pathcontours[path],thinedpath[path])
    # minus = cv2.addWeighted(fullskel,-1,thinedpath[0],1,0)
        endpoints2temp= findendp(fullskel) # หา จุดปลายใหม่ของ เส้นที่ เติมความยาว คอนทัวทั้งหมดแล้ว
        for point in endpoints2temp:
            endpoints2.append(list(point))
        # print('lst=',endpoints2)
        spreadline(endpoints2,fullskel,denoiseimg)
        pathlst.append(fullskel)
    # print("pathlst",len(pathlst))
    fullpath = np.zeros(keepedge.shape, np.uint8)
    for i in range(len(pathlst)):
        fullpath = cv2.addWeighted(fullpath, 1, pathlst[i], 1, 0)
    
    contours2, hierarchy2 = cv2.findContours(fullskel, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    # print("contours2 =",len(contours2))
    famesy = np.zeros(keepedge.shape, np.uint8) # famesy จะรวม path
    cv2.drawContours(famesy,contours2,-1,(255,255,255),3)
    cv2.imshow("myfriend",fullskel)
    # for skel in range(len(contours2)):
    #     epsilon = 0.05*cv2.arcLength(contours2[skel],True)
    #     approx = cv2.approxPolyDP(contours2[skel],epsilon,True)
    # approximg = np.zeros(keepedge.shape, np.uint8)
    # cv2.drawContours(approximg,approx,-1,(255,255,255),3)
    contours3, hierarchy3 = cv2.findContours(fullpath, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    epsilon = 0.0125*cv2.arcLength(contours3[0],True) # index เป็น 0 เพราะรวม path หมดแล้ว
    approx = cv2.approxPolyDP(contours3[0],epsilon,True)
    approximg = np.zeros(keepedge.shape, np.uint8)
    # contours3, hierarchy3 = cv2.findContours(fullpath, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    cv2.drawContours(approximg,approx,-1,(255,255,255),3)
    # print("pointinpath=",len(cornerpoints_skel))
    # print("approx",approx)
    for ap in range(len(approx)):
        if list(approx[ap][0]) not in cornerpoints_skel:
            cornerpoints_skel.append(list(approx[ap][0]))
    # print("pointinpath=",len(cornerpoints_skel))
    # print("endpoint2=",endpoints2)
    for n in range(len(endpoints2)):
        if list(endpoints2[n]) not in cornerpoints_skel:
            end_skel.append(list(endpoints2[n]))
    # print("pointinpath=",len(cornerpoints_skel))
    # ปรับ พิกัดของ endpoints
    for e in end_skel:
        e.reverse()
    for n in range(len(end_skel)):
        if list(end_skel[n]) not in cornerpoints_skel:
            cornerpoints_skel.append(list(end_skel[n]))
    # print("corner=",cornerpoints_skel)
    cv2.imshow("approximg",approximg)
    # print("pointinpath=",len(cornerpoints_skel))
    # return approximg
    pcolor = 5
    for p in range(len(cornerpoints_skel)):
        cv2.circle(clone, (cornerpoints_skel[p][0],cornerpoints_skel[p][1]), 7, (255-(3*pcolor),255-(2*pcolor),255-(pcolor)), -1)
        pcolor+=10
    # cv2.circle(clone, (cornerpoints_skel[-1][0],cornerpoints_skel[-1][1]), 7, (0,255,0), -1)

    ################ Sort point from chessboard ###################################
    stoppoint = centerfinish[0]
    sortpoint.append(stoppoint)
    # print("stop=",stoppoint)
    # print("contours3=",contours3)
    # print("cornerpoint",len(cornerpoints_skel))
    # print(contours2[0][0])
    count = 0
    for p in range(len(contours3[0])):
        for q in range(len(cornerpoints_skel)):
            if count == 0:
                if list(contours3[0][p][0]) == sortpoint[0] :
                    count = 1 
            if count == 1:
                if list(contours3[0][p][0]) == cornerpoints_skel[q] :
                    # print(list(contours2[0][p][0]),cornerpoints_sskel[q])
                    if  cornerpoints_skel[q] not in sortpoint:
                        sortpoint.append(cornerpoints_skel[q])
                        print(cornerpoints_skel[q])
                    if len(sortpoint) == len(cornerpoints_skel):
                        break
    if len(pathcontours) == 1:                    
        for p in range(len(contours3[0])):
            for q in range(len(cornerpoints_skel)):
                if list(contours3[0][p][0]) == cornerpoints_skel[q] :
                    if  cornerpoints_skel[q] not in sortpoint:
                        sortpoint.append(cornerpoints_skel[q])
                        print(cornerpoints_skel[q])
                    if len(sortpoint) == len(cornerpoints_skel):
                        break
    print("sort=",sortpoint)
    qcolor = 5
    clone2 = frame.copy()[cropsize:-cropsize, cropsize:-cropsize]
    nubcircle=0
    for p in range(len(sortpoint)):
        cv2.circle(clone2, (sortpoint[p][0],sortpoint[p][1]), 7, (255-(3*qcolor),255-(2*qcolor),255-(qcolor)), -1)
        nubcircle+=1
        qcolor+=10
    print('circle',nubcircle)
    nubeng =0
    for poi in range(len(sortpoint)-1):
        cv2.line(clone2, (sortpoint[poi][0],sortpoint[poi][1]), (sortpoint[poi+1][0],sortpoint[poi+1][1]), (255,255,255), 1)
        nubeng+=1
    print('nub',nubeng)
    # cv2.circle(clone2, (sortpoint[3][0],sortpoint[3][1]), 7, (0,255,0), -1)

    # ##########################  หามุม ##############################
    # for p in range(len(sortpoint)-1):
    #     ang = math.degrees(math.atan2(sortpoint[p+1][1]-sortpoint[p][1],sortpoint[p+1][0]-sortpoint[p][0]))
    #     if ang < 0 :
    #         ang += 360
    #     # ang+=90
    #     print('p',sortpoint[p])
    #     print('p+1',sortpoint[p+1])
    #     print('now-ang= ',ang)
    #     anglespath.append(ang)
    # ######################### เปลี่ยน coordinate ###################
    # for p in range(len(sortpoint)):
    #     world_position.append(convert_coordinate(sortpoint[p]))
    # print("world_position",world_position)
    # print("anglepath",anglespath)
    # for p in range(len(world_position)-1):
    #     normy = math.sqrt(math.pow((world_position[p+1][1]-world_position[p][1]),2)+math.pow((world_position[p+1][0]-world_position[p][0]),2))
    #     rf_list.append(normy)
    # print(rf_list)
    # print(newimg.shape)
    ################  plot 3d  ######################
    plotmypath(fullpath,denoiseimg,0)
    # contours5, hierarchy5 = cv2.findContours(pathlst[0], cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    # testpathlst= np.zeros(keepedge.shape, np.uint8)
    # cv2.drawContours(testpathlst,contours5,-1,(255,255,255),-1)
    # cv2.imshow('pathlst0',testpathlst)
    # cv2.waitKey(0)
    # return testpathlst
    # print(len(pathlst))
    # if len(pathlst) >= 1:
    for path in range(len(pathlst)): # หาค่า Z มาส่งไป embeded
        kernelc = np.ones((3, 3), np.uint8) / 10
        diratepath = cv2.dilate(pathlst[path], kernelc, iterations= 10)
        cv2.imshow('pathlst0',diratepath )
        cv2.waitKey(0)
        getZ(diratepath,denoiseimg)
    
    count = 0
    while 0 in sortpointZ:
        for num in range(len(sortpointZ)):
            if sortpointZ[num] == 0 and num != (len(sortpointZ)-1):
                sortpointZ[num] = sortpointZ[num+1]
            elif sortpointZ[num] == 0 and num == (len(sortpointZ)-1):
                sortpointZ[num] = sortpointZ[num-1]
        count += 1
        if count > 10:
            break
    print("OMGsortZ=",sortpointZ)

    print('X',X)
    print('Y',Y)
    print('Z',sortpointZ)
    cv2.imshow('grey',newimg)
    cv2.imshow('denosie',denoiseimg)
    cv2.imshow('point',clone)
    cv2.imshow('point2',clone2)
    fig = plt.figure()
    # fig = plt.figure(figsize=plt.figaspect(0.5))
    ax = plt.axes(projection="3d")
    # ax = plt.add_subplot(1, 2, 1, projection='3d')
    
    cv2.imshow('tempfullpath',fullpath)
    # tempfullpath = np.argwhere(fullpath == 255)
    xf,yf = tempfullpath.T
    # ax.plot3D(X, Y, Z, 'gray')
    ax.scatter3D(xf,yf, Z, c=Z, cmap='hsv')
    # ax.set_xlabel('X Label')
    # ax.set_ylabel('Y Label')
    # ax.set_zlabel('Z Label')
    #########################################################
    # Xpoint = []
    # Ypoint = []
    # for point in range(len(sortpoint)):
    #     Xpoint.append(sortpoint[point][0])
    #     Ypoint.append(sortpoint[point][1])
    # # ax = fig.add_subplot(1, 2, 2, projection='3d')
    # print('myX',Xpoint)
    # print('myY',Ypoint)
    ###############################################################
    # ax.plot3D(Ypoint,Xpoint,sortpointZ,label='parametric curve')
    ax.set_xlabel('X Label')
    ax.set_ylabel('Y Label')
    ax.set_zlabel('Z Label')
    plt.show()
    sortpointZ.reverse()
    cv2.waitKey(0)
    print("OMGsortZ=",sortpointZ)
    # ######################## หา traj ให้ แกน z ####################
    # for p in range(len(sortpointZ)-1):
    #     normZ = sortpointZ[p+1]-sortpointZ[p]
    #     rfZ_list.append(normZ)
    # ##############################################################
    clone3 = frame.copy()[cropsize:-cropsize, cropsize:-cropsize]
    ######################### เปลี่ยน coordinate ###################
    sortpoint.reverse()
    for p in range(len(sortpoint)):
        world_position.append(convert_coordinate(sortpoint[p]))
    print("world_position",world_position)
    for p in range(len(world_position)-1):
        normy = math.sqrt(math.pow((world_position[p+1][1]-world_position[p][1]),2)+math.pow((world_position[p+1][0]-world_position[p][0]),2))
        rf_list.append(normy)
    print('rf_list',rf_list)
    # print('rfZ_list',rfZ_list)
    print(newimg.shape)
    ##########################  หามุม ##############################
    for p in range(len(sortpoint)-1):
        ang = math.degrees(math.atan2(sortpoint[p+1][1]-sortpoint[p][1],sortpoint[p+1][0]-sortpoint[p][0]))
        if ang < 0 :
            ang += 360
        # ang+=90
        # print('p',sortpoint[p])
        # print('p+1',sortpoint[p+1])
        # print('now-ang= ',ang)
        anglespath.append(ang)
        anglesZ = anglespath.copy()
        for a in range(len(anglesZ)):
            if anglesZ[a] > 180.0:
                anglesZ[a] -= 180.0
        print("anglepath",anglespath)
        print("angleZ",anglesZ)
    rcolor =5
    for p in range(len(sortpoint)):
        cv2.circle(clone3, (sortpoint[p][0],sortpoint[p][1]), 7, (255-(3*rcolor),255-(2*rcolor),255-(rcolor)), -1)
        rcolor+=10
    
    for poi in range(len(sortpoint)-1):
        cv2.line(clone3, (sortpoint[poi][0],sortpoint[poi][1]), (sortpoint[poi+1][0],sortpoint[poi+1][1]), (255,255,255), 1)
    print('sortpointZ=',sortpointZ)
    return sortpointZ,anglesZ

######################################## main ########################################################
# img = cv2.imread('fieldimages/myfield.png', cv2.IMREAD_COLOR)
img = cv2.imread('fieldimages/myfieldeiei.png', cv2.IMREAD_COLOR)
# img = cv2.imread('fieldimages/myfield22.png', cv2.IMREAD_COLOR)
cv2.namedWindow('tuner')
def nothing(x):
    pass
# create min
cv2.createTrackbar('min','tuner',10,200,nothing)
# create trackbars for max
cv2.createTrackbar('max','tuner',10,200,nothing)
# create tratrackbars for erosion contours
# cv2.createTrackbar('erodeCon','tuner',1,10,nothing)

# while(1):
#     tune1 = cv2.getTrackbarPos('min','tuner')
#     tune2 = cv2.getTrackbarPos('max','tuner')
#     x = img.copy()
#     func = PathFinder(x,tune1,tune2)
#     # func = PathFinder(x) 
#     # cv2.imshow('tuner',func)
#     # cv2.imwrite('fieldimages/adjustfield.png', func) 
#     cv2.waitKey(1)
x = img.copy()
# func = PathFinder(x,tune1,tune2)