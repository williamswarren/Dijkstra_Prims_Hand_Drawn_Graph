# import the necessary packages
from pytesseract import Output
import pytesseract
import argparse
import cv2
import numpy as np

'''
img = "/Users/warrenwilliams/Documents/School/UCSC Extension/Quarter 3/mlproject/research/test_input_images/precise_graph3.png"
img = cv2.imread(img)
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
	if 15 < h < 125 and 15 < w < 125:
		cv2.rectangle(img, (x,y), (x+w, y+h), (255, 0, 255), 1, cv2.LINE_AA)	
		results = pytesseract.image_to_data(img[y:y+h , x:x+w], output_type=Output.DICT)

		# loop over each of the individual text localizations
		for i in range(0, len(results["text"])):
			# extract the bounding box coordinates of the text region from
			# the current result
			x = results["left"][i]
			y = results["top"][i]
			w = results["width"][i]
			h = results["height"][i]
			# extract the OCR text itself along with the confidence of the
			# text localization
			text = results["text"][i]
			conf = int(results["conf"][i])


			# filter out weak confidence text localizations
			if conf > 10:
				# display the confidence and text to our terminal
				print("Confidence: {}".format(conf))
				print("Text: {}".format(text))
				print("")
				# strip out non-ASCII text so we can draw the text on the image
				# using OpenCV, then draw a bounding box around the text along
				# with the text itself
				text = "".join([c if ord(c) < 128 else "" for c in text]).strip()
				cv2.rectangle(img[y:y+h , x:x+w], (x, y), (x + w, y + h), (0, 255, 0), 2)
				cv2.putText(img[y:y+h , x:x+w], text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX,1.2, (0, 0, 255), 3)
				# show the output image
				cv2.imshow("Image", img[y:y+h , x:x+w])
				cv2.waitKey(0)

'''





# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
	help="path to input image to be OCR'd")
ap.add_argument("-c", "--min-conf", type=int, default=0,
	help="mininum confidence value to filter weak text detection")
args = vars(ap.parse_args())

# load the input image, convert it from BGR to RGB channel ordering,
# and use Tesseract to localize each area of text in the input image
image = cv2.imread(args["image"])
rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
rgb = cv2.GaussianBlur(rgb,(11,11),0)
rgb = cv2.medianBlur(rgb,9)



results = pytesseract.image_to_data(rgb, output_type=Output.DICT, config="--psm 12")


# loop over each of the individual text localizations
for i in range(0, len(results["text"])):
	# extract the bounding box coordinates of the text region from
	# the current result
	x = results["left"][i]
	y = results["top"][i]
	w = results["width"][i]
	h = results["height"][i]
	# extract the OCR text itself along with the confidence of the
	# text localization
	text = results["text"][i]
	conf = int(results["conf"][i])


# filter out weak confidence text localizations
	if conf > args["min_conf"]:
		# display the confidence and text to our terminal
		print("Confidence: {}".format(conf))
		print("Text: {}".format(text))
		print("")
		# strip out non-ASCII text so we can draw the text on the image
		# using OpenCV, then draw a bounding box around the text along
		# with the text itself
		text = "".join([c if ord(c) < 128 else "" for c in text]).strip()
		cv2.rectangle(rgb, (x, y), (x + w, y + h), (0, 255, 0), 2)
		cv2.putText(rgb, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX,
			1.2, (0, 0, 255), 3)
# show the output image
cv2.imshow("Image", rgb)
cv2.waitKey(0)




