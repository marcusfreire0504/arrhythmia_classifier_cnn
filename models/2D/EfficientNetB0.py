# -*- coding: utf-8 -*-
"""Untitled0.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1VQES6MVRjqOcRdqcZRcOJNbVKM_jmEm6
"""

from tensorflow.keras.models import Sequential, Model
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import Activation
from tensorflow.keras.layers import Conv2D
from tensorflow.keras.layers import MaxPooling2D
from tensorflow.keras.layers import Dropout
from tensorflow.keras.layers import Flatten
from tensorflow.keras.layers import Input
from tensorflow.keras.layers import BatchNormalization
from tensorflow.python.keras.applications.efficientnet import *

def EfficientNetB0_model(input_shape, n_classes):
  input_tensor = Input(shape=input_shape)
  efficientnet = EfficientNetB0(include_top=False,
                  weights='imagenet',
                  input_tensor=input_tensor)

  top = Sequential()
  top.add(Flatten(input_shape=efficientnet.output_shape[1:]))
  top.add(Dense(256, activation='relu'))
  top.add(Dropout(0.5))
  top.add(Dense(n_classes, activation='softmax'))
  
  model = Model(inputs=efficientnet.input, outputs=top(efficientnet.output))

  return model

if __name__ == '__main__':
  model = EfficientNetB0_model(input_shape=(128, 129, 3), n_classes=5)
  model.summary()