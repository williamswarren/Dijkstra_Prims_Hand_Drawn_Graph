import cv2 as cv
import numpy as np

COLORS_DICT_BGR = {(0, 0, 255):("red", "A"),
    (0, 255, 0):("green", "G"),
    (240, 32, 160):("purple", "C"),
    (42, 42, 165):("brown", "D"),
    (203, 192, 255):("pink", "E"),
    (0, 255, 255):("yellow", "F"),
    (255, 255, 255):("white", "W"),
    (0, 0, 0):("black", "BL"),
    (255, 0, 0):("blue", "B")}



#image = cv.imread("/Users/warrenwilliams/Downloads/graphviz_find_colors.png")

def get_bgr_values(image_path):
	COLORS_DICT = {}
	for row in range(image.shape[0]):
		for col in range(image.shape[1]):
			if tuple(image[row][col]) not in COLORS_DICT:
				COLORS_DICT[tuple(image[row][col])] = 1
			else:
				COLORS_DICT[tuple(image[row][col])] += 1

	for key, value in COLORS_DICT.items():
		if value > 100:
			print(key, value)
	return COLORS_DICT
'''
for row in range(image.shape[0]):
	for col in range(image.shape[1]):
		if tuple(image[row][col]) not in COLORS_DICT_BGR:
			for closest_row in range(row-2, row+3):
				for closest_col in range(col-2, col+3):
					if tuple(image[closest_row][closest_col]) in COLORS_DICT_BGR:
						image[row][col] = image[closest_row][closest_col]

			if tuple(image[row][col]) not in COLORS_DICT_BGR:
				image[row][col] = np.array([0, 0, 0])
'''
def remove_anti_alias(image, COLORS_DICT_BGR):
	for row in range(image.shape[0]-1, -1, -1):
		for col in range(image.shape[1]-1, -1, -1):	
			if tuple(image[row][col]) not in COLORS_DICT_BGR:
				for closest_row in range(row-2, row+3):
					for closest_col in range(col-2, col+3):
						if tuple(image[closest_row][closest_col]) in COLORS_DICT_BGR:
							image[row][col] = image[closest_row][closest_col]

				if tuple(image[row][col]) not in COLORS_DICT_BGR:
					image[row][col] = np.array([0, 0, 0])
	return image




for image in range(1,8):
	str = f"/Users/warrenwilliams/Documents/School/UCSC Extension/Quarter 3/mlproject/graphviz_images/graphviz_find_colors{image}.png"
	new_image = cv.imread(str)
	processed_image = remove_anti_alias(new_image, COLORS_DICT_BGR)
	new_str = f"/Users/warrenwilliams/Documents/School/UCSC Extension/Quarter 3/mlproject/graphviz_images/graphviz_find_colors_processed{image}.png"	
	cv.imwrite(new_str, processed_image)
	





#cv.imwrite("/Users/warrenwilliams/Downloads/graphviz_c2_edited2.png", image)


