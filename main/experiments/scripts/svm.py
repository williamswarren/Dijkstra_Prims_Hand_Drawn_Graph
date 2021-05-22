from sklearn import datasets   ## importing datasets from sklearn
import cv2 as cv
import numpy as np
digits = datasets.load_digits()  ### loading data from scikit_learn library

from sklearn import svm

svc = svm.SVC(gamma=0.001, C=100.)

print(digits.data[0])

svc.fit(digits.data[:1438], digits.target[:1438])  ## fitting on training set

y_pred = svc.predict(digits.data[1438:1796])  ## making prediction on validation set

y_test = digits.target[1438:1796]

from sklearn.metrics import accuracy_score, classification_report
print(accuracy_score(y_test,y_pred))
print(classification_report(y_test,y_pred))






test_image = cv.imread("/Users/warrenwilliams/Documents/School/UCSC Extension/Quarter 3/mlproject/research/scripts/dst.png")

slice_array = []

test_array = [(2382, 3789, 26, 58),
(2177, 3738, 40, 77),
(2288, 3543, 31, 52),
(2332, 3231, 27, 89),
(2602, 3211, 57, 151),
(1951, 2703, 28, 170),
(1883, 2655, 60, 180),
(2926, 2577, 37, 68),
(2976, 2442, 45, 109),
(339, 2385, 132, 306),
(2523, 2353, 156, 223),
(2852, 2264, 172, 194),
(2755, 2117, 269, 128),
(2963, 1909, 61, 33),
(1170, 1813, 50, 176),
(2137, 1801, 136, 179),
(807, 1634, 39, 141),
(1076, 1271, 161, 149),
(466, 952, 41, 116),
(308, 779, 67, 200),
(1738, 652, 129, 154),
(2859, 585, 69, 119)]

crop_image_array = []
for values in test_array:
	crop_image_array.append(test_image[values[1]:values[1]+values[3], values[0]:values[0]+values[2]])

	from sklearn.preprocessing import MinMaxScaler
	data = cv.resize(test_image[values[1]:values[1]+values[3], values[0]:values[0]+values[2]], dsize=(8, 8), interpolation=cv.INTER_CUBIC).reshape(-1,64)
	scaler = MinMaxScaler(feature_range=(0,15))
	scaler.fit(data)
	result = scaler.transform(data)

	#slice_array.append(cv.resize(test_image[values[1]:values[1]+values[3], values[0]:values[0]+values[2]], dsize=(8, 8)).reshape(-1,64)) #.astype(np.float32))
	slice_array.append(result)








print(slice_array)
#save formated numbers

for index, nums in enumerate(crop_image_array):
	string = f"num_slice{index}.png"
	cv.imwrite(string, nums)

slice_array = np.array(slice_array)
print(slice_array)
for index, slices in enumerate(slice_array):
	y_pred = svc.predict(slices)
	print(y_pred)
	print(index, "*************************")
