# -*- coding: utf-8 -*-
"""Training.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1XyIuJMETOUguKOcpBET8pQTjMmRpqrD0
"""

import numpy as np
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras import optimizers
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau, ModelCheckpoint
from sklearn.metrics import classification_report, multilabel_confusion_matrix, confusion_matrix,f1_score, accuracy_score, recall_score, precision_score
from imblearn.metrics import specificity_score

from VGG16 import vgg16_model

#normalização
train_generator = ImageDataGenerator(rotation_range = 7,
                                     horizontal_flip = True, shear_range = 0.2,
                                     height_shift_range = 0.07, zoom_range = 0.2)

test_generator = ImageDataGenerator(rotation_range = 7, horizontal_flip = True,
                                    shear_range = 0.2, height_shift_range = 0.07,
                                    zoom_range = 0.2)

train_data_generator = train_generator.flow_from_directory('/content/drive/My Drive/TCC_IC_2020/ecg_img/split10percent/train')

test_data_generator = test_generator.flow_from_directory('/content/drive/My Drive/TCC_IC_2020/ecg_img/split10percent/test')

model = vgg16_model(input_shape=(256, 256, 3), n_classes=5)
opt = optimizers.Adam(lr = 0.05)
model.compile(optimizer = opt, loss = 'categorical_crossentropy', metrics = ['accuracy'])

es = EarlyStopping(monitor='accuracy', mode="max", patience=5, verbose=1)
rlr = ReduceLROnPlateau(monitor='accuracy', mode="max", patience=5, verbose=2)
checkpoint = ModelCheckpoint(filepath ='pesos.h5', monitor='accuracy', verbose=1, save_best_only=True, mode='max')
callbacks_list = [checkpoint, es, rlr]

history = model.fit_generator(train_data_generator, epochs= 50, steps_per_epoch=(train_data_generator.samples/train_data_generator.batch_size), 
                                      validation_data = test_data_generator, validation_steps=(test_data_generator.samples/test_data_generator.batch_size))

#model.load_weights('pesos.h5')

#Confution Matrix and Classification Report
test_steps_per_epoch = np.math.ceil(test_data_generator.samples/test_data_generator.batch_size)

predictions = model.predict_generator(test_data_generator, steps=test_steps_per_epoch)
# Get most likely class
predicted_classes = np.argmax(predictions, axis=1)

true_classes = test_data_generator.classes
class_labels = list(test_data_generator.class_indices.keys()) 

print('Matriz de Confusão')
print(multilabel_confusion_matrix(true_classes, predicted_classes))

print('Matriz de Confusão')
print(confusion_matrix(true_classes, predicted_classes))

print('Accuracia')
print(accuracy_score(true_classes, predicted_classes))

print('Sensibilidade')
print(recall_score(true_classes, predicted_classes, average='micro'))
print(recall_score(true_classes, predicted_classes, average='macro'))

print('Precisão')
print(precision_score(true_classes, predicted_classes, average='micro'))
print(precision_score(true_classes, predicted_classes, average='macro'))

print('Especificidade')
print(specificity_score(true_classes, predicted_classes, average='micro'))
print(specificity_score(true_classes, predicted_classes, average='macro'))

print('F1-score')
print(f1_score(true_classes, predicted_classes, average='micro')) 
print(f1_score(true_classes, predicted_classes, average='macro')) 

#GRÁFICO PARA COMPARAR RESULTADOS DO TESTE
import matplotlib.pyplot as plt

gof_train_acc  = history.history['accuracy']
gof_train_loss = history.history['loss'    ]
gof_valid_acc  = history.history['val_accuracy' ]
gof_valid_loss = history.history['val_loss']
epochs = range(len(gof_train_acc))

# Graph Accuracy
plt.figure(figsize = (15,5))
plt.plot(epochs, gof_train_acc, 'b', label = 'Training')
plt.plot(epochs, gof_valid_acc, 'r', label = 'Validation')
plt.title('Accuracy')
plt.legend()
plt.show()

# Graph Loss
plt.figure(figsize = (15,5))
plt.plot(epochs, gof_train_loss, 'b', label = 'Training')
plt.plot(epochs, gof_valid_loss, 'r', label = 'Validation')
plt.title('Loss')
plt.legend()
plt.show()

plt.figure(figsize = (15,5))
plt.plot(predictions, test_data_generator, 'b', label = 'Training')
plt.title('Loss')
plt.legend()
plt.show()