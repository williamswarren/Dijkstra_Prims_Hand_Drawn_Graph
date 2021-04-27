import cv2
import numpy as np
from matplotlib import pyplot as plt

img = cv2.imread('../test_input_images/test_graph.jpg',0)

sobelx = cv2.Sobel(img,cv2.CV_64F,1,0,ksize=5)

plt.subplot(2,2,1),plt.imshow(img,cmap = 'gray')
plt.title('Original'), plt.xticks([]), plt.yticks([])
plt.subplot(2,2,3),plt.imshow(sobelx,cmap = 'gray')
plt.title('Sobel X'), plt.xticks([]), plt.yticks([])

cv2.imwrite("../test_output_images/sobelx_image_gradient.jpg",sobelx)

plt.show()


edges = cv2.Canny(img,190,200)
cv2.imwrite('../test_output_images/canny_edge_graph.jpg',edges)
plt.subplot(121),plt.imshow(img,cmap = 'gray')
plt.title('Original Image'), plt.xticks([]), plt.yticks([])
plt.subplot(122),plt.imshow(edges,cmap = 'gray')
plt.title('Edge Image'), plt.xticks([]), plt.yticks([])

plt.show()
