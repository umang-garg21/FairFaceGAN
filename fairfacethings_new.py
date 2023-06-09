# -*- coding: utf-8 -*-
"""Fairfacethings.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1uQpZgdHyWtKR_5Om0EsBMaUp80aq15jk
"""

from google.colab import drive
drive.mount('/content/drive')

import zipfile
!unzip /content/drive/MyDrive/fairfacefolder/fairface-img-margin025-trainval.zip

!unzip /content/drive/MyDrive/fairfacefolder/imgs_jpg.zip

!unzip /content/drive/MyDrive/fairfacefolder/vgg_face_weights.zip

!unzip /content/drive/MyDrive/fairfacefolder/fairface_label_train_w_synth.zip
!unzip /content/drive/MyDrive/fairfacefolder/fairface_label_val.zip
!unzip /content/drive/MyDrive/fairfacefolder/fairface_label_train.zip

import numpy as np
import pandas as pd
import tensorflow as tf
from tqdm import tqdm
import keras.utils as image
from sklearn.model_selection import train_test_split
import time
import matplotlib.pyplot as plt
import cv2

import tensorflow as tf
tf.test.gpu_device_name()

tqdm.pandas()

"""Select which type of data to use. """

train_df = pd.read_csv("fairface_label_train_w_synth.csv")
test_df = pd.read_csv("fairface_label_val.csv", nrows = 5000)
white_a = []
all_races = {'White' : 1000,'Black': 1000,'Latino_Hispanic': 1000,'Southeast Asian': 500,'East Asian': 500,'Indian': 1000,'Middle Eastern': 6000,
             'S_White' : 0,'S_Black': 0,'S_Latino_Hispanic': 0,'S_Southeast Asian': 0,'S_East Asian': 0,'S_Indian': 0,'S_Middle Eastern': 0}

#print(all_races)


# Real White
white_a = pd.read_csv("fairface_label_train_w_synth.csv")
white_a.drop(train_df.index[(train_df['race'] != 'White')],axis=0,inplace=True)
white_a = white_a.reset_index(drop = True)
white_a = white_a.drop(labels = range(all_races['White'],white_a.shape[0]))

#Synthetic White
white_s = pd.read_csv("fairface_label_train_w_synth.csv")
white_s = white_s.drop(train_df.index[(train_df['age'] != '-1')],axis=0)
white_s.drop(white_s.index[(white_s['race'] != 'White')],axis=0, inplace = True)
white_s = white_s.reset_index(drop = True)
white_s = white_a.drop(labels = range(all_races['S_White'],white_a.shape[0]))


# Real Black
black_a = pd.read_csv("fairface_label_train_w_synth.csv")
black_a.drop(train_df.index[(train_df['race'] != 'Black')],axis=0,inplace=True)
black_a = black_a.reset_index(drop = True)
black_a = black_a.drop(labels = range(all_races['Black'],black_a.shape[0]))

# Synthetic Black
black_s = pd.read_csv("fairface_label_train_w_synth.csv")
black_s = black_s.drop(train_df.index[(train_df['age'] != '-1')],axis=0)
black_s.drop(black_s.index[(black_s['race'] != 'Black')],axis=0, inplace = True)
black_s = black_s.reset_index(drop = True)
black_s = black_a.drop(labels = range(all_races['S_Black'],black_a.shape[0]))

# Real Latino
latino_a = pd.read_csv("fairface_label_train_w_synth.csv")
latino_a.drop(train_df.index[(train_df['race'] != 'Latino_Hispanic')],axis=0,inplace=True)
latino_a = latino_a.reset_index(drop = True)
latino_a = latino_a.drop(labels = range(all_races['Latino_Hispanic'],latino_a.shape[0]))

# Synthetic Latino
latino_s = pd.read_csv("fairface_label_train_w_synth.csv")
latino_s = latino_s.drop(train_df.index[(train_df['age'] != '-1')],axis=0)
latino_s.drop(latino_s.index[(latino_s['race'] != 'Latino_Hispanic')],axis=0, inplace = True)
latino_s = latino_s.reset_index(drop = True)
latino_s = latino_a.drop(labels = range(all_races['S_Latino_Hispanic'],latino_a.shape[0]))

# Real Southeast
south_a = pd.read_csv("fairface_label_train_w_synth.csv")
south_a.drop(train_df.index[(train_df['race'] != 'Southeast Asian')],axis=0,inplace=True)
south_a = south_a.reset_index(drop = True)
south_a = south_a.drop(labels = range(all_races['Southeast Asian'],south_a.shape[0]))

#Synthetic Southeat
south_s = pd.read_csv("fairface_label_train_w_synth.csv")
south_s = south_s.drop(train_df.index[(train_df['age'] != '-1')],axis=0)
south_s.drop(south_s.index[(south_s['race'] != 'Southeast Asian')],axis=0, inplace = True)
south_s = south_s.reset_index(drop = True)
south_s = south_a.drop(labels = range(all_races['S_Southeast Asian'],south_a.shape[0]))

# Real East
east_a = pd.read_csv("fairface_label_train_w_synth.csv")
east_a.drop(train_df.index[(train_df['race'] != 'East Asian')],axis=0,inplace=True)
east_a = east_a.reset_index(drop = True)
east_a = east_a.drop(labels = range(all_races['East Asian'],east_a.shape[0]))

# Synthetic East
east_s = pd.read_csv("fairface_label_train_w_synth.csv")
east_s = east_s.drop(train_df.index[(train_df['age'] != '-1')],axis=0)
east_s.drop(east_s.index[(east_s['race'] != 'East Asian')],axis=0, inplace = True)
east_s = east_s.reset_index(drop = True)
east_s = east_a.drop(labels = range(all_races['S_East Asian'],east_a.shape[0]))

#Real Indian
indian_a = pd.read_csv("fairface_label_train_w_synth.csv")
indian_a.drop(train_df.index[(train_df['race'] != 'Indian')],axis=0,inplace=True)
indian_a = indian_a.reset_index(drop = True)
indian_a = indian_a.drop(labels = range(all_races['Indian'],indian_a.shape[0]))

#Synthetic Indian
indian_s = pd.read_csv("fairface_label_train_w_synth.csv")
indian_s = indian_s.drop(train_df.index[(train_df['age'] != '-1')],axis=0)
indian_s.drop(indian_s.index[(indian_s['race'] != 'Indian')],axis=0, inplace = True)
indian_s = indian_s.reset_index(drop = True)
indian_s = indian_a.drop(labels = range(all_races['S_Indian'],indian_a.shape[0]))

#Real Middle
middle_a = pd.read_csv("fairface_label_train_w_synth.csv")
middle_a.drop(train_df.index[(train_df['race'] != 'Middle Eastern')],axis=0,inplace=True)
middle_a = middle_a.reset_index(drop = True)
middle_a = middle_a.drop(labels = range(all_races['Middle Eastern'],middle_a.shape[0]))

#Synthetic Middle
middle_s = pd.read_csv("fairface_label_train_w_synth.csv")
middle_s = middle_s.drop(train_df.index[(train_df['age'] != '-1')],axis=0)
middle_s.drop(middle_s.index[(middle_s['race'] != 'Middle Eastern')],axis=0, inplace = True)
middle_s = middle_s.reset_index(drop = True)
middle_s = middle_a.drop(labels = range(all_races['S_Middle Eastern'],middle_a.shape[0]))

del train_df
combined = [white_a, black_a, latino_a, south_a, east_a, indian_a, middle_a, white_s, black_s, latino_s, south_s, east_s, indian_s, middle_s]
train_df = pd.concat(combined, ignore_index = True)
#train_df = train_df.reset_index(drop = True)
print(train_df)

print("trainset consists of ",train_df.shape)
print("test set consist of ",test_df.shape)

# Uncomment for race
train_df = train_df[['file', 'race']]
test_df = test_df[['file', 'race']]

# train_df = train_df[['file', 'gender']]
# test_df = test_df[['file', 'gender']]

train_df['file'] = 'FairFace/'+train_df['file']
test_df['file'] = 'FairFace/'+test_df['file']

train_df.head()
# There are 2 races as East and Southeast Asian. Group them in a single Asian Race
# uncomment for race
idx = train_df[(train_df['race'] == 'East Asian') | (train_df['race'] == 'Southeast Asian')].index
train_df.loc[idx, 'race'] = 'Asian'

idx = test_df[(test_df['race'] == 'East Asian') | (test_df['race'] == 'Southeast Asian')].index
test_df.loc[idx, 'race'] = 'Asian'

100*train_df.groupby(['race']).count()[['file']]/train_df.groupby(['race']).count()[['file']].sum()
#100*train_df.groupby(['gender']).count()[['file']]/train_df.groupby(['gender']).count()[['file']].sum()

target_size = (224, 224)

def getImagePixels(file):
    #print(file)
    img = image.load_img(file, grayscale=False, target_size=target_size)
    x = image.img_to_array(img).reshape(1, -1)[0]
    return x

#make sure to Create a Folder called 'FairFace' and place the val, train, and imgs_jpg' folders inside

train_df['pixels'] = train_df['file'].progress_apply(getImagePixels)
test_df['pixels'] = test_df['file'].progress_apply(getImagePixels)

train_df.head()

train_features = []; test_features = []

for i in range(0, train_df.shape[0]):
    train_features.append(train_df['pixels'].values[i])

for i in range(0, test_df.shape[0]):
    test_features.append(test_df['pixels'].values[i])

tic = time.time()

train_features = np.array(train_features)
train_features = train_features.reshape(train_features.shape[0], 224, 224, 3)

test_features = np.array(test_features)
test_features = test_features.reshape(test_features.shape[0], 224, 224, 3)

toc = time.time()

print("converted to numpy in ",toc-tic,"seconds")

tic = time.time()

train_features = train_features / 255
test_features = test_features / 255

toc = time.time()

print("converted to numpy in ",toc-tic,"seconds")

train_label = train_df[['race']]
test_label = test_df[['race']]

# train_label = train_df[['gender']]
# test_label = test_df[['gender']]

races = train_df['race'].unique()
# print(genders)
#races = ['White','Black','Latino_Hispanic','Middle Eastern','Indian','Asian']

for j in range(len(races)): #label encoding
    current_race = races[j]
    print("replacing ",current_race," to ", j+1)
    train_label['race'] = train_label['race'].replace(current_race, str(j+1))
    test_label['race'] = test_label['race'].replace(current_race, str(j+1))

train_label = train_label.astype({'race': 'int32'})
test_label = test_label.astype({'race': 'int32'})

# for j in range(len(genders)): #label encoding
#     current_gender = genders[j]
#     print("replacing ",current_gender," to ", j+1)
#     train_label['gender'] = train_label['gender'].replace(current_gender, str(j+1))
#     test_label['gender'] = test_label['gender'].replace(current_gender, str(j+1))

# train_label = train_label.astype({'gender': 'int32'})
# test_label = test_label.astype({'gender': 'int32'})

train_label.head()

train_target = pd.get_dummies(train_label['race'], prefix='race')
test_target = pd.get_dummies(test_label['race'], prefix='race')

# train_target = pd.get_dummies(train_label['gender'], prefix='gender')
# test_target = pd.get_dummies(test_label['gender'], prefix='gender')

train_target.head()

train_x, val_x, train_y, val_y = train_test_split(train_features, train_target.values
                                        , test_size=0.3, random_state=17)

import keras
from keras.preprocessing import image
from keras.callbacks import ModelCheckpoint,EarlyStopping
from keras.layers import Dense, Activation, Dropout, Flatten, Input, Convolution2D, ZeroPadding2D, MaxPooling2D, Activation
from keras.layers import Conv2D, AveragePooling2D
from keras.models import Model, Sequential

#VGG-Face model
model = Sequential()
model.add(ZeroPadding2D((1,1),input_shape=(224,224, 3)))
model.add(Convolution2D(64, (3, 3), activation='relu'))
model.add(ZeroPadding2D((1,1)))
model.add(Convolution2D(64, (3, 3), activation='relu'))
model.add(MaxPooling2D((2,2), strides=(2,2)))
 
model.add(ZeroPadding2D((1,1)))
model.add(Convolution2D(128, (3, 3), activation='relu'))
model.add(ZeroPadding2D((1,1)))
model.add(Convolution2D(128, (3, 3), activation='relu'))
model.add(MaxPooling2D((2,2), strides=(2,2)))
 
model.add(ZeroPadding2D((1,1)))
model.add(Convolution2D(256, (3, 3), activation='relu'))
model.add(ZeroPadding2D((1,1)))
model.add(Convolution2D(256, (3, 3), activation='relu'))
model.add(ZeroPadding2D((1,1)))
model.add(Convolution2D(256, (3, 3), activation='relu'))
model.add(MaxPooling2D((2,2), strides=(2,2)))
 
model.add(ZeroPadding2D((1,1)))
model.add(Convolution2D(512, (3, 3), activation='relu'))
model.add(ZeroPadding2D((1,1)))
model.add(Convolution2D(512, (3, 3), activation='relu'))
model.add(ZeroPadding2D((1,1)))
model.add(Convolution2D(512, (3, 3), activation='relu'))
model.add(MaxPooling2D((2,2), strides=(2,2)))
 
model.add(ZeroPadding2D((1,1)))
model.add(Convolution2D(512, (3, 3), activation='relu'))
model.add(ZeroPadding2D((1,1)))
model.add(Convolution2D(512, (3, 3), activation='relu'))
model.add(ZeroPadding2D((1,1)))
model.add(Convolution2D(512, (3, 3), activation='relu'))
model.add(MaxPooling2D((2,2), strides=(2,2)))
 
model.add(Convolution2D(4096, (7, 7), activation='relu'))
model.add(Dropout(0.5))
model.add(Convolution2D(4096, (1, 1), activation='relu'))
model.add(Dropout(0.5))
model.add(Convolution2D(2622, (1, 1)))
model.add(Flatten())
model.add(Activation('softmax'))

#pre-trained weights of vgg-face model. 
#you can find it here: https://drive.google.com/file/d/1CPSeum3HpopfomUEK1gybeuIVoeJT_Eo/view?usp=sharing
#related blog post: https://sefiks.com/2018/08/06/deep-face-recognition-with-keras/
model.load_weights('vgg_face_weights.h5')

num_of_classes = 6#len(races)

#freeze all layers of VGG-Face except last 7 one
for layer in model.layers[:-7]:
    layer.trainable = False

base_model_output = Sequential()
base_model_output = Convolution2D(num_of_classes, (1, 1), name='predictions')(model.layers[-4].output)
base_model_output = Flatten()(base_model_output)
base_model_output = Activation('softmax')(base_model_output)

race_model = Model(inputs=model.input, outputs=base_model_output)

race_model.compile(loss='categorical_crossentropy'
                  , optimizer=keras.optimizers.Adam()
                  , metrics=['accuracy']
                 )

checkpointer = ModelCheckpoint(
    filepath='race_model_single_batch.hdf5'
    , monitor = "val_loss"
    , verbose=1
    , save_best_only=True
    , mode = 'auto'
)

patience = 20

val_scores = []; train_scores = []

enableBatch = True

epochs = 100

if enableBatch != True:
    early_stop = EarlyStopping(monitor='val_loss', patience=patience) 
    
    score = race_model.fit(
        train_x, train_y
        , epochs=epochs
        , validation_data=(val_x, val_y)
        , callbacks=[checkpointer, early_stop]
    )
    
else:
    batch_size = pow(2, 9)
    last_improvement = 0
    best_iteration = 0
    
    loss = 1000000 #initialize as a large value
    
    for i in range(0, epochs):
        
        print("Epoch ", i, ". ", end='')
        
        ix_train = np.random.choice(train_x.shape[0], size=batch_size)
        
        score = race_model.fit(
            train_x[ix_train], train_y[ix_train]
            , epochs=1
            , validation_data=(val_x, val_y)
            , callbacks=[checkpointer]
        )
        
        val_loss = score.history['val_loss'][0]
        train_loss = score.history['loss'][0]
        
        val_scores.append(val_loss)
        train_scores.append(train_loss)
        
        #--------------------------------
        
        if val_loss < loss:
            loss = val_loss * 1
            last_improvement = 0
            best_iteration = i * 1
        else:
            last_improvement = last_improvement + 1
            print("try to decrease val loss for ",patience - last_improvement," epochs more")
        
        #--------------------------------
        
        if last_improvement == patience:
            print("there is no loss decrease in validation for ",patience," epochs. early stopped")
            break

if enableBatch != True:
    plt.plot(score.history['val_loss'], label='val_loss')
    plt.plot(score.history['loss'], label='train_loss')
    plt.legend(loc='upper right')
    plt.show()
else:
    plt.plot(val_scores[0:best_iteration], label='val_loss')
    plt.plot(train_scores[0:best_iteration], label='train_loss')
    plt.legend(loc='upper right')
    plt.show()

if enableBatch != True:
    plt.plot(score.history['val_loss'][0:best_iteration], label='val_loss')
    plt.plot(score.history['loss'][0:best_iteration], label='train_loss')
    plt.legend(loc='upper right')
    plt.show()
else:
    plt.plot(val_scores[0:best_iteration+1], label='val_loss')
    plt.plot(train_scores[0:best_iteration+1], label='train_loss')
    plt.legend(loc='upper right')
    plt.show()

from keras.models import load_model
race_model = load_model("race_model_single_batch.hdf5")

race_model.save_weights('race_model_single_batch.h5')

# test_perf = race_model.evaluate(test_features, test_target.values, verbose=1)
# print(test_perf)

# validation_perf = race_model.evaluate(val_x, val_y, verbose=1)
# print(validation_perf)

#Check model is robust
# abs(validation_perf[0] - test_perf[0]) < 0.01

predictions = race_model.predict(test_features)

prediction_classes = []; actual_classes = []
right = []; wrong = []
print(predictions.shape[0])
for i in range(0, predictions.shape[0]):
    prediction = np.argmax(predictions[i])
    prediction_classes.append(races[prediction])
    actual = np.argmax(test_target.values[i])
    actual_classes.append(races[actual])

    # if (genders[actual] != genders[prediction]):
    #     wrong.append(i)
    # else:
    #     right.append(i)


 
    # if i in range(0,100):
    #     # 375, 470, 750, 758, 875, 992, 1061, 2181, 2255, 4725, 4944 #latino
    #     # , 124, 339, 762, 913, 1340, 1363, 2205 #black
    #     # , 33, 83, 237, 609, 817, 1223, 1377 #asian
    #     # , 109, 203, 899, 1094, 1180, 1250, 1395, 1556 #indian
    #     # , 638, 718, 1088, 1460, 4396, 4477 #middle eastern
    #     # , 413, 447, 573, 649, 723, 1258, 1274, 1430, 1485 #white
    #     # , 17, 235, #misclassified
    #     print(i)
    #     print("Actual: ",genders[actual])
    #     print("Predicted: ",genders[prediction])
        
    #     img = (test_df.iloc[i]['pixels'].reshape([224, 224, 3])) / 255
    #     plt.imshow(img)
    #     plt.show()
    #     print("----------------------")

# # Code to get wrongly predicted by race
# # we have array of right[] and wrong[] with index i
# fresh_val = pd.read_csv("fairface_label_val.csv")
# #print(fresh_val.shape)
# white_count = 0
# black_count = 0
# southeast_count = 0
# latino_count = 0
# indian_count = 0
# middle_count = 0
# eastern_count = 0

# white_count_w = 0
# black_count_w = 0
# southeast_count_w = 0
# latino_count_w = 0
# indian_count_w = 0
# middle_count_w = 0
# eastern_count_w = 0

# for i in wrong[:]:
#   race_val = fresh_val.iloc[i+1][3]
  
#   if race_val == 'White':
#     white_count_w += 1
#   if race_val == 'Black':
#     black_count_w += 1
#   if race_val == 'Southeast Asian':
#     southeast_count_w += 1
#   if race_val == 'Latino_Hispanic':
#     latino_count_w += 1
#   if race_val == 'Indian':
#     indian_count_w += 1
#   if race_val == 'Middle Eastern':
#     middle_count_w += 1
#   if race_val == 'East Asian':
#     eastern_count_w += 1

# for i in right[:-1]:
#   race_val = fresh_val.iloc[i+1][3]
#   #print(f' {i} {fresh_val.iloc[i]}')
  
#   if race_val == 'White':
#     white_count += 1
#   if race_val == 'Black':
#     black_count += 1
#   if race_val == 'Southeast Asian':
#     southeast_count += 1
#   if race_val == 'Latino_Hispanic':
#     latino_count += 1
#   if race_val == 'Indian':
#     indian_count += 1
#   if race_val == 'Middle Eastern':
#     middle_count += 1
#   if race_val == 'East Asian':
#     eastern_count += 1

# print(f'{white_count} {black_count} {southeast_count} {latino_count} {indian_count} {middle_count} {eastern_count}')
# print(f'{white_count_w} {black_count_w} {southeast_count_w} {latino_count_w} {indian_count_w} {middle_count_w} {eastern_count_w}')
# print(f'{white_count/( white_count+white_count_w )} {black_count/(black_count + black_count_w)} {southeast_count/(southeast_count + southeast_count_w)} {latino_count/( latino_count+ latino_count_w)} {indian_count/(indian_count + indian_count_w)} {middle_count/( middle_count+ middle_count_w)} {eastern_count/( eastern_count+ eastern_count_w)}')
# #compared = (actual_classes == prediction_classes)
# #for row in compared is not False:

from sklearn.metrics import classification_report, confusion_matrix
import seaborn as sn

cm = confusion_matrix(actual_classes, prediction_classes)

cm

df_cm = pd.DataFrame(cm, index=races, columns=races)

sn.heatmap(df_cm, annot=True,annot_kws={"size": 10})