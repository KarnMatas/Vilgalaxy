import cv2
import numpy as np
# credit arduino map func
def map(x, in_min, in_max, out_min, out_max):
  return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

count = 0
Shape_list = []
Card_list = []
img = cv2.imread('module.png')
imgGrey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
gray_blur = cv2.GaussianBlur(imgGrey, (7, 7), 0)
# cv2.imshow("img", gray_blur)
kernel = np.ones((5,5),np.float32)/25
average = cv2.filter2D(imgGrey,-1,kernel)
edge = cv2.Canny(average, 200, 100)
dilation = cv2.dilate(edge,kernel,iterations = 1)
erosion = cv2.erode(dilation,kernel,iterations = 1)
# cv2.imshow("shapes", edge)
# cv2.waitKey(0)
contours, hierarchy = cv2.findContours(erosion, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

kernel = np.ones((5,5),np.float32)/25
average = cv2.filter2D(imgGrey,-1,kernel)
# find contour for paths
myContours = []
for cnt,hir in zip(contours,hierarchy[0]):
    if hir[2] == -1:
        if cv2.contourArea(cnt) >= 10000:
            myContours.append(cnt)
newDraw = np.zeros(img.shape,np.uint8)
cv2.drawContours(newDraw, myContours, -1, (255,255,255), -1)
cv2.imshow("dark",newDraw)
pathlst = []
for path in range(len(myContours)):
    pathlst.append(np.zeros((img.shape[0],img.shape[1]),np.uint8))  # greyscale เพราะมี กว้าง กับ ยาว
    cv2.drawContours(pathlst[path], myContours, path, 255, -1)
    pathlst[path] = cv2.erode(pathlst[path],kernel,iterations = 5)
    # cv2.imshow("path",pathlst[path])
    # cv2.waitKey(0)
# หา ค่า min max ของ gradient pixel
minpix = []
maxpix = []
keepixel = []
for i in range(len(pathlst)):
    temp = np.argwhere(pathlst[i] == 255)
    for j in temp:
        keepixel.append(imgGrey[j[0],j[1]])
    maxpix.append(max(keepixel))
    minpix.append(min(keepixel))
    keepixel = []
# print([maxpix,minpix])
outlinePath = []
pathdraw = np.zeros((img.shape[0],img.shape[1]),np.uint8)
for cnt,hir in zip(contours,hierarchy[0]):
    if hir[3] == -1:
        outlinePath.append(cnt)
        cv2.drawContours(pathdraw, outlinePath,-1, 255, -1)
# cv2.imshow("and",pathdraw)
# cv2.waitKey(0)
# print(pathdraw.shape)
# หา skeleton
thinned = cv2.ximgproc.thinning(pathdraw)
for i in pathlst:
    i =  cv2.bitwise_and(i,thinned)
    cv2.imshow("and",i)
    cv2.waitKey(0)
# map ค่า   
X = []
Y = []
Z = [] # lb = 10 cm. ub = 20 cm.
rawZ = []
for i in range(len(pathlst)):
    temp2 = np.argwhere(pathlst[1] == 255)    
    for j in temp2:
        X.append(j[0])
        Y.append(j[1])
        rawZ.append(imgGrey[j[0],j[1]])
    for k in rawZ:
        if (maxpix[2]-minpix[2]) > 10.0:
            Z.append(map(k,minpix[1],maxpix[1],10.0,20.0))
            # print([maxpix[2],minpix[2],k,map(k,minpix[2],maxpix[2],10.0,20.0)])
    rawZ=[]
# print(maxpix[0],minpix[0]) 
cv2.waitKey(0)


# part detect edge and shape
for i in range(0, len(contours)):
    # collect Poly
    approx = cv2.approxPolyDP(contours[i], 0.01 * cv2.arcLength(contours[i], True), True)
    # edge = cv2.Canny(gray, 100, 20)
    # ================= Draw Poly ================================
    # line = cv2.drawContours(img, [approx], 0, (0, 0, count), 5)
    # filled = cv2.fillPoly(img, [approx], (0, count, 0))
    count += 25
    # cv2.imshow("shapes", line)
#     # area
    area = cv2.contourArea(contours[i])
    findchild = hierarchy[0][i][2]
    child = []
    while findchild != -1:
        child.append(findchild)
        findchild = hierarchy[0][findchild][2]

    if len(approx) == 4 & findchild != -1:
        x1 = approx[0][0][0] if approx[0][0][0] > approx[3][0][0] else approx[3][0][0]
        x2 = approx[1][0][0] if approx[1][0][0] > approx[2][0][0] else approx[2][0][0]
        y1 = approx[0][0][1] if approx[0][0][1] > approx[1][0][1] else approx[1][0][1]
        y2 = approx[2][0][1] if approx[2][0][1] > approx[3][0][1] else approx[3][0][1]
        crop_img = img[y1:y2,x1:x2]

        Card_list.append(dict(Area=area, Approx=[approx],Contour=[contours[i]], Child=child, X1=x1,X2=x2,Y1=y1,Y2=y2,Crop=crop_img))
        Shape_list.append(dict(Area=area, Contour=[contours[i]], Child=child))
    else:
        Shape_list.append(dict(Area=area, Contour=[contours[i]], Child=child))
    # print(hierarchy)
for card_num in range(len(Card_list)):
    crop = Card_list[card_num]["Crop"]
    cv2.imshow("cropped " + str(card_num), crop)
    
    cv2.drawContours(img, Card_list[card_num]["Approx"], 0, (0, 0, 255), 7)
    for i in Card_list[card_num]["Child"]:
        # print(i)
        line = cv2.drawContours(img, Shape_list[i]["Contour"], 0, (0, 0, 255), 5)
for i in range(0,len(contours)): # เช็ค คอนทัว
    cv2.drawContours(img,contours,i,(0,0,255))
    cv2.imshow("shapes", img)
    cv2.waitKey(0)

# cv2.imshow("shapes", img)
# cv2.waitKey(0)
cv2.destroyAllWindows()

# =============================================================================

findPath = Card_list[0]