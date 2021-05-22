import numpy as np
import cv2 as cv

img = cv.imread('./digits.png')
gray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)

# Now we split the image to 5000 cells, each 20x20 size
cells = [np.hsplit(row,100) for row in np.vsplit(gray,50)]

# Make it into a Numpy array: its size will be (50,100,20,20)
x = np.array(cells)

# Now we prepare the training data and test data
train = x[:,:50].reshape(-1,400).astype(np.float32) # Size = (2500,400)
test = x[:,50:100].reshape(-1,400).astype(np.float32) # Size = (2500,400)

# Create labels for train and test data
k = np.arange(10)
train_labels = np.repeat(k,250)[:,np.newaxis]
test_labels = train_labels.copy()

# Initiate kNN, train it on the training data, then test it with the test data with k=1
knn = cv.ml.KNearest_create()
knn.train(train, cv.ml.ROW_SAMPLE, train_labels)
ret,result,neighbours,dist = knn.findNearest(test,k=5)

# Now we check the accuracy of classification
# For that, compare the result with test_labels and check which are wrong
matches = result==test_labels
correct = np.count_nonzero(matches)
accuracy = correct*100.0/result.size
print( accuracy )
print(result)
print(train[0])
print(train_labels[0])

test_image = cv.imread("/Users/warrenwilliams/Documents/School/UCSC Extension/Quarter 3/mlproject/research/scripts/dst.png")
#test_image = cv.cvtColor(cv.bitwise_not(test_image), cv.COLOR_BGR2GRAY)

#REMOVE ANTI-ALIASING FROM IMAGE
for row in range(test_image.shape[0]-1, -1, -1):
	for col in range(test_image.shape[1]-1, -1, -1):
		if sum(tuple(test_image[row][col])) > 300:
			test_image[row][col] = np.array([0, 0, 0])
		else:
			test_image[row][col] = np.array([255, 255, 255])

cv.imwrite("black_white.png", test_image) 

test_image = cv.cvtColor(test_image,cv.COLOR_BGR2GRAY)
#test_image = cv.bitwise_not(test_image)
#print(test)

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
	slice_array.append(cv.resize(test_image[values[1]:values[1]+values[3], values[0]:values[0]+values[2]], (20, 20), interpolation = cv.INTER_AREA).reshape(-1,400).astype(np.float32))

print(slice_array)
#save formated numbers

for index, nums in enumerate(crop_image_array):
	string = f"num_slice{index}.png"
	cv.imwrite(string, nums)

slice_array = np.array(slice_array)
print(slice_array)
for index, slices in enumerate(slice_array):
	ret, result, neighbors, dist = knn.findNearest(slices, k=11)
	print(result)
	print(index, "*************************")
print(test_labels)


# Save the data
np.savez('knn_data.npz',train=train, train_labels=train_labels)
# Now load the data
with np.load('knn_data.npz') as data:
    print( data.files )
    train = data['train']
    train_labels = data['train_labels']
	
