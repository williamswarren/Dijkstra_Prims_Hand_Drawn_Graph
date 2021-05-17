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

test_image = cv.imread("/Users/warrenwilliams/Documents/School/UCSC Extension/Quarter 3/mlproject/research/scripts/morphed2.png")

slice_array = []

test_array = [(1284, 1685, 20, 87),
(1565, 1120, 71, 74),
(1227, 502, 50, 74),
(604, 1401, 73, 95),
(1450, 818, 82, 82),
(1466, 831, 53, 55),
(404, 815, 46, 49),
(406, 765, 42, 42),
(993, 1604, 75, 78),
(1008, 1105, 19, 81),
(951, 528, 68, 70),
(703, 1016, 22, 81),
(672, 529, 17, 74),
(878, 192, 30, 60)
]

crop_image_array = []
for values in test_array:
	crop_image_array.append(test_image[values[1]:values[1]+values[3], values[0]:values[0]+values[2]])
	slice_array.append(cv.resize(test_image[values[1]:values[1]+values[3], values[0]:values[0]+values[2]], (20, 20), interpolation = cv.INTER_AREA).reshape(-1,400).astype(np.float32))

print(slice_array)
#save formated numbers

for index, nums in enumerate(crop_image_array):
	string = f"num_slice_improved{index}.png"
	cv.imwrite(string, nums)

slice_array = np.array(slice_array)
print(slice_array)
for index, slices in enumerate(slice_array):
	ret, result, neighbors, dist = knn.findNearest(slices, k=5)
	print(index, "*************************")
	print(result)
print(test_labels)


# Save the data
np.savez('knn_data.npz',train=train, train_labels=train_labels)
# Now load the data
with np.load('knn_data.npz') as data:
    print( data.files )
    train = data['train']
    train_labels = data['train_labels']
	
