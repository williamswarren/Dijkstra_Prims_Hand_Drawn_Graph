'''
import numpy as np
import cv2

img = cv2.imread('../test_output_images/canny_edgeBINARY_INV.jpg', cv2.IMREAD_GRAYSCALE)
ret,thresh = cv2.threshold(img,127,255,0)
#image, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
contours,hierachy=cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
#cnt = contours[4]
#img = cv2.drawContours(img, [cnt], 0, (0,255,0), 3)
'''
import numpy as np
import cv2 as cv
im = cv.imread('../test_output_images/canny_edgeBINARY_INV.jpg')
imgray = cv.cvtColor(im, cv.COLOR_BGR2GRAY)
ret, thresh = cv.threshold(imgray, 127, 255, 0)
contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
im = cv.drawContours(im, contours, -1, (0,255,0), 3)
cv.imwrite('../test_output_images/contour_graph.jpg',im)
cv.imshow('image',im)
cv.waitKey(0)
cv.destroyAllWindows()
