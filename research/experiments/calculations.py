import numpy as np
import cv2 as cv
im = cv.imread('BINARY_INV.jpg')
imgray = cv.cvtColor(im, cv.COLOR_BGR2GRAY)
ret, thresh = cv.threshold(imgray, 127, 255, 0)
contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
print(len(contours))
count = 0
circle_list = []
for cnt in range(len(contours)):

   if cv.contourArea(contours[cnt]) > 165:
      circle_list.append(contours[cnt])
      count += 1
      print('Index: ', cnt)
      print('Moments: ', cv.moments(contours[cnt]))
      print('Area: ', cv.contourArea(contours[cnt]))
      print('Perimeter: ', cv.arcLength(contours[cnt],True))
      epsilon = 0.1*cv.arcLength(contours[cnt],True)
      print('Contour Approx: ', epsilon)
      print('Contour Approx 2: ', cv.approxPolyDP(contours[cnt],epsilon,True))
print(count)
#im = cv.drawContours(im, contours, -1, (0,255,0), 3)

im = cv.drawContours(im, circle_list, -1, (0,255,0), 3)
#cv.imwrite('contour_graph.jpg',im) #uncomment to write
cv.imshow('image',im)
cv.waitKey(0)
cv.destroyAllWindows()
