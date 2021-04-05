import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt

mnist = tf.keras.datasets.fashion_mnist

(trainImages, trainLabels), (testImages,testLabels) = mnist.load_data()
#print(trainImages.shape, len(trainLabels))

"""plt.figure()
plt.imshow(trainImages[0])
plt.colorbar()
plt.grid(False)
plt.show()"""

trainImages = trainImages / 255.0
testImages = testImages / 255.0

"""
classNames = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat',
               'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']

plt.figure(figsize=(10,10))
for i in range(25):
	plt.subplot(5,5,i+1)
	plt.xticks([])
	plt.yticks([])
	plt.grid(False)
	plt.imshow(trainImages[i], cmap=plt.cm.binary)
	plt.xlabel(classNames[trainLabels[i]])
plt.show()
"""

model = tf.keras.Sequential([
	tf.keras.layers.Flatten(input_shape=(28,28)),
	tf.keras.layers.Dense(128, activation='relu'),
	tf.keras.layers.Dense(10)
])

model.compile(
	optimizer='adam',
	loss = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
	metrics = ['accuracy']
)

model.fit(trainImages,trainLabels,epochs=16)

testLoss, testAcc = model.evaluate(testImages, testLabels, verbose=2)
print("Accuracy: ",testAcc)