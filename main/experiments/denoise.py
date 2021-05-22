import numpy as np
import cv2
from matplotlib import pyplot as plt
img = cv2.imread('output.jpg')
median = cv2.medianBlur(img,5)
blur = cv2.bilateralFilter(img,9,75,75)  
cv2.imwrite('denoised.jpg',median)  
# Plotting of source and destination image
plt.subplot(121), plt.imshow(median)
plt.subplot(122), plt.imshow(blur)
  
plt.show()
