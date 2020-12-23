import numpy as np
import cv2 
import matplotlib.pyplot as plt
card = cv2.imread('fieldimages/sun.png',cv2.IMREAD_GRAYSCALE)          # queryImage
field = cv2.imread('fieldimages/mycard.png',cv2.IMREAD_GRAYSCALE) # trainImage
################################
def match_symbol(base_im,sym_im):
    if (len(base_im.shape)) != 2:
        base_im = cv2.cvtColor(base_im,cv2.COLOR_BGR2GRAY)

    if (len(sym_im.shape)) != 2:
        sym_im = cv2.cvtColor(sym_im,cv2.COLOR_BGR2GRAY)

    # Initiate SIFT detector
    sift = cv2.SIFT_create()
    # find the keypoints and descriptors with SIFT
    kp1, des1 = sift.detectAndCompute(base_im,None)
    kp2, des2 = sift.detectAndCompute(sym_im,None)

    # FLANN parameters
    FLANN_INDEX_KDTREE = 1
    index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
    search_params = dict(checks=200)   # or pass empty dictionary
    flann = cv2.FlannBasedMatcher(index_params,search_params)
    matches = flann.knnMatch(des1,des2,k=2)
    good = []
    for m,n in matches:
        if m.distance < 0.1*n.distance:
            good.append(m)
    x = 0
    y = 0
    points = [kp1[m.queryIdx].pt for m in good ]
    for point in points:
        x += point[0]
        y += point[1]
    x = int(x/len(points))
    y = int(y/len(points))
    map_buf = base_im.copy()
    return [x,y]

point = match_symbol(field,card)
cv2.circle(field, (point[0],point[1]), 7, (0,0,0), -1)
cv2.imshow('fil',field)
cv2.waitKey(0)