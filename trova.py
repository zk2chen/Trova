# -*- coding: utf-8 -*-
"""Trova.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/12zXJ7kESMtG6tmdZ8KZE8Ji00cTE4Bg6
"""

#keras 
from keras.models import Sequential
from keras.layers import Dense, Conv2D, Flatten, MaxPooling2D, Activation, Dropout
from keras.optimizers import adam, RMSprop
from keras.utils import np_utils
from keras.preprocessing.image import ImageDataGenerator

from sklearn.utils import shuffle
from sklearn.model_selection import train_test_split

#Import libraries
import numpy as np
import matplotlib.pyplot as plt
import os
import cv2

from google.colab import drive

#Get content from google drive
from google.colab import drive
drive.mount('/content/drive')

#Accessing the dataset
PATH = os.getcwd()
trova_data_path = PATH + '/drive/My Drive/Colab_Notebooks/Official-Dataset'
list_of_folders = os.listdir(trova_data_path)
print(list_of_folders)

image_labels = {'Bike': 0, 'Bollard': 1, 'Calculator': 2,
               'Camera': 3, 'Chair':4,
              'Coffee mug': 5, 'Computer keyboard': 6, 'Computer mouse': 7, 
                'Earphones': 8, 'Filing cabinet': 9, 'Glasses': 10, 'Headphones': 11,
                'Laptop': 12, 'Manhole cover': 13, 'Pay phone': 14,
                'Handicap button': 15, 'Remote control': 16, 'Ruler': 17, 'Scissors': 18,
                'Wet floor sign':19, 'Stapler': 20, 'Crosswalk button': 21,
                 'Tennis ball': 22, 'Toaster': 23, 'Traffic cone': 24, 'Wallet': 25,
                'Watch':26, 'Flashlight': 27, 'Table lamp': 28, 'Printer': 29, 'Stop sign': 30,
                'Fire hydrant': 31, 'Traffic light': 32, 'Car': 33, 'Bus': 34, 'License plate': 35,
                'Lamp post': 36, 'Newspaper boxes': 37, 'Parking meter': 38, 'Briefcase': 39, 
                'Combo lock': 40, 'Paper clip': 41, 'Light switch': 42, 'Wooden pencil': 43, 
                'Binder clips': 44, 'Vending machine': 45, 'Sneaker': 46, 'Bench':47, 'Backpack': 48,
                'Pen': 49
              }

list_of_images = []
list_of_labels = []

img_rows = 128
img_cols = 128

channel_num = 1
num_of_classes = 24

for folders in list_of_folders:
  image_list = os.listdir(trova_data_path + '/' + folders)
  print('loading images for ' + folders)
  labels = image_labels[folders]
  
  for images in image_list:
    input_image = cv2.imread(trova_data_path + '/' + folders + '/' + images)
    input_image = cv2.cvtColor(input_image, cv2.COLOR_BGR2GRAY)
    input_image_resized = cv2.resize(input_image, (img_rows, img_cols))
    
    list_of_images.append(input_image_resized)
    list_of_labels.append(labels)

#convert the image list to an array and convert it to float32
image_array = np.array(list_of_images)
image_array = image_array.astype('float32')

image_array = image_array/255

print(image_array.shape)

#Convert the labels list to an array and convert the labels to one hot encoding
label_array = np.array(list_of_labels)
labels_one_hot = np_utils.to_categorical(label_array, num_of_classes)

#Shuffle image dataset and split it into testing and training sets
x,y = shuffle(image_array, labels_one_hot, random_state = 2)

X_train, X_test, y_train, y_test = train_test_split(x,y, test_size = 0.2, random_state = 2)

print(X_train.shape)

print(X_test.shape)

plt.imshow(X_train[22])

plt.imshow(X_train[222])

#reshape the image sets to fit the model
X_train = X_train.reshape(29130, 128,128,1)
X_test = X_test.reshape(7283, 128,128,1)

#Build the model

model = Sequential()

model.add(Conv2D(32, kernel_size= (3,3), padding='SAME',input_shape= [128,128,1])) #55 #33 
model.add(Activation('relu'))
model.add(Conv2D(32, kernel_size = (3,3), padding = 'SAME')) #55
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))

model.add(Conv2D(64, kernel_size= (3,3), padding ='SAME',input_shape= [128,128,1])) #33
model.add(Activation('relu'))
model.add(Conv2D(64, kernel_size= (3,3), padding ='SAME')) #33
model.add(Activation('relu'))

model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Conv2D(64, kernel_size = (3,3), padding = 'SAME', input_shape = [128,128,1]))
model.add(Activation('relu'))
model.add(Conv2D(64, kernel_size = (3,3), padding = 'SAME', input_shape = [128,128,1]))
model.add(Activation('relu'))
model.add(Dropout(0.25))
model.add(MaxPooling2D(pool_size=(2,2)))


model.add(Flatten())
model.add(Dense(1000)) 
model.add(Activation('relu'))
##model.add(Dropout(0.25))
model.add(Dense(num_of_classes))
model.add(Activation('softmax'))

#Compile the model

model.compile(optimizer= 'rmsprop', loss = 'categorical_crossentropy',
             metrics = ['accuracy'])

#Data Augmentation to avoid overfitting

datagen = ImageDataGenerator(
      featurewise_center = False,
      samplewise_center = False,
      featurewise_std_normalization = False,
      samplewise_std_normalization = False,
      zca_whitening = False,
      rotation_range = 10,
      zoom_range = 0.1,
      width_shift_range = 0.1,
      height_shift_range = 0.1,
      horizontal_flip = False,
      vertical_flip = False
)

datagen.fit(X_train)



#Fit the model
model.fit_generator(datagen.flow(X_train,y_train, batch_size= 50),
                              epochs = 20, validation_data = (X_test,y_test),
                              verbose = 2, steps_per_epoch=X_train.shape[0] // 50
                              )

#hist = model.fit(X_train, y_train, batch_size=50, epochs=20, verbose=1, validation_data=(X_test, y_test))

#Compare to actual first 10 images in test set
test_image = X_test[0:1]
print(test_image.shape)

#Evaluate the model
score = model.evaluate(X_test, y_test, verbose = 0 )
print('Test loss:', score[0])
print('Test accuracy:', score[1])

print(model.predict(test_image))

print(model.predict_classes(test_image))

print(y_test[0:1])







