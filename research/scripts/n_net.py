from keras.datasets import mnist

(x_train, y_train), (x_test, y_test) = mnist.load_data()

# save input image dimensions
img_rows, img_cols = 28, 28

x_train = x_train.reshape(x_train.shape[0], img_rows, img_cols, 1)
x_test = x_test.reshape(x_test.shape[0], img_rows, img_cols, 1)

x_train //= 255
x_test //= 255

from tensorflow.keras.utils import to_categorical
num_classes = 10

y_train = to_categorical(y_train, num_classes)
y_test = to_categorical(y_test, num_classes)

from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten, Conv2D, MaxPooling2D

model = Sequential()
model.add(Conv2D(32, kernel_size=(3, 3),
     activation='relu',
     input_shape=(img_rows, img_cols, 1)))


model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Dropout(0.25))

model.add(Flatten())

model.add(Dense(128, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(num_classes, activation='softmax'))

model.compile(loss='sparse_categorical_crossentropy',
      optimizer='adam',
      metrics=['accuracy'])

batch_size = 128
epochs = 10

model.fit(x_train, y_train,
          batch_size=batch_size,
          epochs=epochs,
          verbose=1,
          validation_data=(x_test, y_test))
score = model.evaluate(x_test, y_test, verbose=0)
print('Test loss:', score[0])
print('Test accuracy:', score[1])
model.save("test_model.h5")

'''
Bring in Test images
'''

test_image = cv.imread("/Users/warrenwilliams/Documents/School/UCSC Extension/Quarter 3/mlproject/research/scripts/dst.png")
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
    slice_array.append(cv.resize(test_image[values[1]:values[1]+values[3], values[0]:values[0]+values[2]], (28, 28)).reshape(-1,784).astype(np.float32))

for item in slice_array:
	# reshape the image
	gray = item

	# normalize image
	gray /= 255

	# predict digit
	prediction = model.predict(gray)
	print(prediction.argmax())
