import cv2
import numpy as np

# (1) src 
#img = cv2.imread("/Users/warrenwilliams/Documents/School/UCSC Extension/Quarter 3/mlproject/research/test_output_images/TRUNC2.jpg")
img = cv2.imread("../test_input_images/precise_graph3.png")
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# (2) threshold-inv and morph-open 
th, threshed = cv2.threshold(gray, 100, 255, cv2.THRESH_OTSU|cv2.THRESH_BINARY_INV)
morphed = cv2.morphologyEx(threshed, cv2.MORPH_OPEN, np.ones((2,2)))
# (3) find and filter contours, then draw on src 
cnts = cv2.findContours(morphed, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[-2]


nh, nw = img.shape[:2]
#print(cnts)
for cnt in cnts:
	x,y,w,h = bbox = cv2.boundingRect(cnt)
	#print(bbox)
	#print("height", h)
	if 15 < h < 100 and 15 < w < 100:
		cv2.rectangle(img, (x,y), (x+w, y+h), (255, 0, 255), 1, cv2.LINE_AA)
		print(bbox)

cv2.imwrite("dst2.png", img)
cv2.imwrite("morphed2.png", morphed)

