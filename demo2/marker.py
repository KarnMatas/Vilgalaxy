import numpy as np
import cv2
import cv2.aruco as aruco
from math import floor
# frame = cv2.imread("aruco3.jpg") #aruco3
# cap = cv2.VideoCapture(0 + cv2.CAP_DSHOW)
# cap.set(3, 1280) # set the resolution
# cap.set(4, 720)
# cap.set(cv2.CAP_PROP_AUTOFOCUS, 0)
side0=[]
side1=[]
side2=[]
side3=[]
field_corners=[]
amount = 30
center_p = []
aruco_id = { 
            }
listofimages =[]


def onlyminmax(side):
    l = min(side)
    h = max(side)
    side = []
    side.append(l)
    side.append(h)
    return side

def callaruco(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    aruco_dict = aruco.Dictionary_get(aruco.DICT_4X4_250)
    arucoParameters = aruco.DetectorParameters_create()
    corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=arucoParameters)
    for id in range(len(corners)):
        x_c = int((corners[id][0][0][0]+ corners[id][0][1][0]+ corners[id][0][2][0]+ corners[id][0][3][0])/4)
        y_c = int((corners[id][0][0][1]+ corners[id][0][1][1]+ corners[id][0][2][1]+ corners[id][0][3][1])/4)
        center_p.append([x_c,y_c])
        aruco_id[ids[id][0]] = [x_c,y_c]
        # if   floor(ids[id][0] / 4 )== 0:
        #     side0.append(ids[id][0])
        # elif floor(ids[id][0] / 4 )== 1:
        #     side1.append(ids[id][0])
        # elif floor(ids[id][0] / 4 )== 2:
        #     side2.append(ids[id][0])
        # elif floor(ids[id][0] / 4 )>= 3:
        #     side3.append(ids[id][0])
        if  ids[id][0] / 4.0 <= 1:
            side0.append(ids[id][0])
        elif ids[id][0] / 4.0 <= 2:
            side1.append(ids[id][0])
        elif ids[id][0] / 4.0 <= 3:
            side2.append(ids[id][0])
        elif ids[id][0] / 4.0  <= 4:
            side3.append(ids[id][0])
    # print(corners[0],ids[0][0])
    # for x in aruco_id:
    #     print(x,aruco_id[x])
    frame = aruco.drawDetectedMarkers(frame, corners) # ใส่ให้ปริ้น ids ด้วยได้
    return frame

def center_of_aruco(frame):
    # print(len(center_p))
    for n in range(len(center_p)):
        cv2.circle(frame, (center_p[n][0], center_p[n][1]), 3, (0, 255, 0), -1)

#([x, y], [x2, y2])

def line_intersection(line1, line2):
    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if div == 0:
       raise Exception('lines do not intersect')

    d = (det(*line1), det(*line2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    return [int(x), int(y)]

def addfield_corners():
    field_corners.append(line_intersection( [ aruco_id[side0[1]], aruco_id[side0[0]] ] , [ aruco_id[side1[1]], aruco_id[side1[0]] ]   )) # right - left
    field_corners.append(line_intersection( [ aruco_id[side1[1]], aruco_id[side1[0]] ] , [ aruco_id[side2[1]], aruco_id[side2[0]] ]   ))
    field_corners.append(line_intersection( [ aruco_id[side2[1]], aruco_id[side2[0]] ] , [ aruco_id[side3[1]], aruco_id[side3[0]] ]   ))
    field_corners.append(line_intersection( [ aruco_id[side3[1]], aruco_id[side3[0]] ] , [ aruco_id[side0[1]], aruco_id[side0[0]] ]   ))

def point_field_corners(frame,ls):
    for n in range(len(ls)):
        cv2.circle(frame, (ls[n][0], ls[n][1]), 3, (0, 0, 255), -1)

def perspective(frame,pixel_x,pixel_y,field_corners):
    length_x = pixel_x
    length_y = pixel_y
    # print("fieldcorner=",field_corners)
    x_pix = np.float32([ [field_corners[0][0], field_corners[0][1]], [field_corners[1][0], field_corners[1][1]], [field_corners[3][0], field_corners[3][1]], [field_corners[2][0], field_corners[2][1]] ])
    y_pix = np.float32([ [0,0], [length_x, 0], [0, length_y], [length_x,length_y] ])
    # x_pix = np.float32([ [field_corners[2][0], field_corners[2][1]], [field_corners[1][0], field_corners[1][1]], [field_corners[0][0], field_corners[0][1]], [field_corners[3][0], field_corners[3][1]] ])
    # y_pix = np.float32([ [0,0], [length_x, 0], [length_x,length_y], [0, length_y] ])
    matrix = cv2.getPerspectiveTransform(x_pix, y_pix)
    result = cv2.warpPerspective(frame, matrix, (length_x,length_y))
    return result

def forget_that_rail():
    images_of_field = tuple(listofimages)
    stackimgs = np.stack(images_of_field, axis=3)
    result = np.median(stackimgs, axis=3).astype(np.uint8)
    return result
    
def cropimg(frame):
    global side0,side1,side2,side3,field_corners
    myaruco = callaruco(frame)
    # cv2.imshow('eiei', myaruco)
    # cv2.waitKey(0)
    # addp = center_of_aruco(myaruco)
    side0=onlyminmax(side0)
    side1=onlyminmax(side1)
    side2=onlyminmax(side2)
    side3=onlyminmax(side3)
    # print("side0:",side0)
    # print("side1:",side1)
    # print("side2:",side2)
    # print("side3:",side3)
    addfield_corners()
    # print(field_corners)
    point_field_corners(myaruco, field_corners)
    perspected = perspective(myaruco,600,600,field_corners)
    # cv2.imshow('drawaruco', myaruco)
    # cv2.imshow('perspected', perspected)
    field_corners = []
    side0 = []
    side1 = []
    side2 = []
    side3 = []
    center_p = []
    aruco_id = { 
                }
    # cv2.waitKey(0)
    cv2.destroyAllWindows()
    return perspected


# while (len(listofimages) != amount):
#     # print("Karn")
#     ret, frame = cap.read()
#     cv2.imshow("raw",frame)
#     wait = cv2.waitKey(1) 
#     # print(wait,ord('c'))
#     if (wait == ord('c')):
#         # print("karn")
#         ret, img = cap.read()
#         cv2.imshow("raw2",img)
#         try :
#             chkpic = img.copy()
#             test = cropimg(chkpic)
#             cv2.imshow("test",test)
#             listofimages.append(img)
#             print(len(listofimages))
#             cv2.waitKey(1000) 
#         except :
#             print("recapture")
#             pass
#     else:
#         pass
# # for i in range(amount):
# #     cv2.imshow("pic",listofimages[i])
# #     cv2.waitKey(0)
# # print(len(listofimages))
# # print("side0:",side0)
# # print("side1:",side1)
# # print("side2:",side2)
# # print("side3:",side3)
# for img in range(len(listofimages)):
#     apic = cropimg(listofimages[img])
#     # listofimages.append(apic)
#     listofimages[img] = apic
#     print(len(listofimages))
#     # cv2.imshow("photy",listofimages[img])
#     print("Karn"+str(img))
#     # cv2.waitKey(2000)
#     cv2.destroyAllWindows()
# norail = forget_that_rail()  
# cv2.imwrite('fieldimages/myfieldgogo.png', norail) 
# cv2.imshow("oyi",norail)
# cv2.waitKey(0)

