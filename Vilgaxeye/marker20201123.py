import numpy as np
import cv2
import cv2.aruco as aruco
from math import floor
# frame = cv2.imread("aruco3.jpg") #aruco3
cap = cv2.VideoCapture(1 + cv2.CAP_DSHOW)
prev_img = np.zeros([100,100,3],dtype=np.uint8)
side0=[]
side1=[]
side2=[]
side3=[]
field_corners=[]
iterations = 5
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
    x_pix = np.float32([ [field_corners[0][0], field_corners[0][1]], [field_corners[1][0], field_corners[1][1]], [field_corners[3][0], field_corners[3][1]], [field_corners[2][0], field_corners[2][1]] ])
    y_pix = np.float32([ [0,0], [length_x, 0], [0, length_y], [length_x,length_y] ])
    matrix = cv2.getPerspectiveTransform(x_pix, y_pix)
    result = cv2.warpPerspective(frame, matrix, (length_x,length_y))
    return result

def forget_that_rail():
    images_of_field = tuple(listofimages)
    stackimgs = np.stack(images_of_field, axis=3)
    result = np.median(stackimgs, axis=3).astype(np.uint8)
    return result
def take_a_picture(frame):
    global side0,side1,side2,side3,field_corners
    myaruco = callaruco(frame)
    # cv2.imshow('eiei', myaruco)
    cv2.waitKey(0)
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
    perspected = perspective(myaruco,700,700,field_corners)
    cv2.imshow('eiei', myaruco)
    # cv2.imshow('perspected', perspected)
    field_corners = []
    side0 = []
    side1 = []
    side2 = []
    side3 = []
    center_p = []
    aruco_id = { 
                }
    cv2.waitKey(0)
    return perspected

# cap = cv2.VideoCapture(1 + cv2.CAP_DSHOW)
ret, frame = cap.read()
height = frame.shape[0]
width = frame.shape[1]
channels = frame.shape[2]
prev_img  =np.ones(shape=[height, width, channels], dtype=np.uint8)
# for n in range(iterations):
#     ret, frame = cap.read()
#     if np.all(prev_img) == np.all(frame):
#         print("yeah")
#         prev_img = frame
#     else:
#         print("Nani!!")
#     # cv2.imshow('sad',frame)
# #     cv2.waitKey(0)
#     apic = take_a_picture(frame)
#     listofimages.append(apic)
#     print(len(listofimages))
#     cv2.imshow("photy",listofimages[n])
#     print("Karn"+str(n))
#     cv2.waitKey(2000)
#     prev_img = frame
#     cv2.destroyAllWindows()


while (len(listofimages) != iterations):
    if len(listofimages) == 0:
        if np.all(prev_img) != np.all(frame):
            print("yeah")
            # ret, frame = cap.read()
            apic = take_a_picture(frame)
            listofimages.append(apic)
            print(len(listofimages))
            cv2.imshow("photy",listofimages[len(listofimages)-1])
            print("Karn"+str(len(listofimages)-1))
            cv2.waitKey(2000)
            cv2.destroyAllWindows()
            prev_img = frame
        # else:
        #     print("Nani!!")
        #     continue
    if len(listofimages) > 0:
        ret, frame = cap.read()
        cv2.imshow("now",frame)
        if np.all(prev_img) != np.all(frame):
            print("yeah")
            # ret, frame = cap.read()
            try:
                apic = take_a_picture(frame)
                listofimages.append(apic)
                print(len(listofimages))
                cv2.imshow("photy",listofimages[len(listofimages)-1])
                print("Karn"+str(len(listofimages)-1))
                cv2.waitKey(2000)
                cv2.destroyAllWindows()
                prev_img = frame
            except:
                continue
        # else:
        #     print("Nani!!")
        #     continue


norail = forget_that_rail()
cv2.imshow("oyi",norail)
cv2.waitKey(0)
# cap = cv2.VideoCapture(1 + cv2.CAP_DSHOW)
# ret, frame = cap.read()
# apic = take_a_picture(frame)
# cv2.imshow("eiei",apic)
# # cap = cv2.VideoCapture(1 + cv2.CAP_DSHOW)
# # ret, frame = cap.read()
# # while(True):
#     # ret, frame = cap.read()
# myaruco = callaruco(frame)
# # print(center_p)
# # cv2.circle(frame, (468, 540), 3, (0, 255, 0), -1)
# addp = center_of_aruco(myaruco)
# side0=onlyminmax(side0)
# side1=onlyminmax(side1)
# side2=onlyminmax(side2)
# side3=onlyminmax(side3)
# addfield_corners()
# # print(side0,side1,side2,side3)
# print(field_corners)
# point_field_corners(myaruco, field_corners)
# perspected = perspective(myaruco,700,700,field_corners)
# cv2.imshow('eiei', myaruco)
# cv2.imshow('perspected', perspected)
# cv2.waitKey(0)
# # perspected = perspective(myaruco,810,540,center_p)
# # cv2.imshow('Display', perspected
#     # cv2.destroyAllWindows()


# # cv2.imshow('Display', frame)
# # if cv2.waitKey(1) & 0xFF == ord('q'):
# #     break
# # cap.release()



# lengthx = 810
# lengthy = 540
# frame = cv2.imread("markertest.jpg")
# gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
# aruco_dict = aruco.Dictionary_get(aruco.DICT_5X5_1000)
# arucoParameters = aruco.DetectorParameters_create()
# corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=arucoParameters)
# center_p =[]
# for i in range(len(corners)):
#     x_c = int((corners[i][0][0][0]+ corners[i][0][1][0]+ corners[i][0][2][0]+ corners[i][0][3][0])/4)
#     y_c = int((corners[i][0][0][1]+ corners[i][0][1][1]+ corners[i][0][2][1]+ corners[i][0][3][1])/4)
#     center_p.append([x_c,y_c])
# print(center_p)
# frame = aruco.drawDetectedMarkers(frame, corners)
# # print(frame)
# xpix = np.float32([ [center_p[2][0], center_p[2][1]], [center_p[1][0], center_p[1][1]], [center_p[3][0], center_p[3][1]], [center_p[0][0], center_p[0][1]] ])
# ypix = np.float32([ [0,0], [lengthx, 0], [0, lengthy], [lengthx,lengthy] ])
# cv2.circle(frame, (center_p[0][0], center_p[0][1]), 3, (0, 255, 0), -1)
# cv2.circle(frame, (center_p[1][0], center_p[1][1]), 3, (0, 255, 0), -1)
# cv2.circle(frame, (center_p[2][0], center_p[2][1]), 3, (0, 255, 0), -1)
# cv2.circle(frame, (center_p[3][0], center_p[3][1]), 3, (0, 255, 0), -1)
# matrix = cv2.getPerspectiveTransform(xpix, ypix)
# result = cv2.warpPerspective(frame, matrix, (lengthx,lengthy))

# set_of_image_to_stack = tuple(after_perspective_transform)
# # for img in after_perspective_transform:
# sequence = np.stack(set_of_image_to_stack, axis=3)
# result = np.median(sequence, axis=3).astype(np.uint8)