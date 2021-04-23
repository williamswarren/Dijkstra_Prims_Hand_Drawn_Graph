import cv2
import numpy as np
image = cv2.imread('test_graph.jpg')
lower_white = np.array([0, 0, 0], dtype=np.uint8)
upper_white = np.array([20, 20, 20], dtype=np.uint8)
mask = cv2.inRange(image, lower_white, upper_white) # could also use threshold
res = cv2.bitwise_and(image, image, mask)

img2gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
ret, mask = cv2.threshold(img2gray, 10, 255, cv2.THRESH_BINARY)
mask_inv = cv2.bitwise_not(mask)
cv2.imshow('mask', mask_inv)

cv2.imshow('res', res) # gives black background

'''
img = cv2.imread('test_graph.jpg')
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
lower_gray = np.array([0, 5, 50], np.uint8)
upper_gray = np.array([179, 50, 255], np.uint8)
mask_gray = cv2.inRange(hsv, lower_gray, upper_gray)
img_res = cv2.bitwise_and(img, img, mask = mask_gray)

cv2.imshow('res',img_res)
cv2.waitKey(0)
cv2.destroyAllWindows()
'''

'''
# define range of blue color in HSV
lower_black = np.array([0,0,0])
upper_black = np.array([10,10,10])
mask = cv2.inRange(hsv, (min_blue, min_green, min_red), (max_blue, max_green, max_red))
#showing the mask image
cv2.imshow('Mask Image', mask)

# Threshold the HSV image to get only blue colors
mask = cv2.inRange(hsv, lower_black, upper_black)

# Bitwise-AND mask and original image
res = cv2.bitwise_and(img,img, mask= mask)

cv2.imshow('frame',hsv)
cv2.imshow('mask',mask)
cv2.imshow('res',res)
'''
cv2.waitKey(0)
cv2.destroyAllWindows()
