
import cv2
import numpy as np

#img = cv2.imread('../test_input_images/test_graph.jpg',0)
img = cv2.imread('../test_input_images/precise_graph2.png', 0)
img = cv2.medianBlur(img,5)
cimg = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)

circles = cv2.HoughCircles(img,cv2.HOUGH_GRADIENT,1,100,
                            param1=80,param2=40,minRadius=100,maxRadius=550)

circles = np.uint16(np.around(circles))
for i in circles[0,:]:
    # draw the outer circle
    cv2.circle(cimg,(i[0],i[1]),i[2],(0,255,0),2)
    # draw the center of the circle
    cv2.circle(cimg,(i[0],i[1]),2,(0,0,255),3)
cv2.imwrite("../test_output_images/houghcircles3.png",cimg)
cv2.imshow('detected circles',cimg)
cv2.waitKey(0)
cv2.destroyAllWindows()
