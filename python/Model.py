import warnings
import pandas as pd
import numpy as np
import random as python_random
import pickle
import os


from sklearn.metrics import classification_report
from sklearn.utils import class_weight
from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split

import tensorflow as tf
import keras
from keras.utils import to_categorical
from keras.models import load_model
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.optimizers import Adam
from keras.callbacks import ModelCheckpoint



class Model:

    def __init__(self):
        warnings.filterwarnings("ignore")
        np.random.seed(42)
        python_random.seed(42)

        if os.path.exists(os.path.join('modelFit','pca.sav')) and os.path.exists(os.path.join('modelFit','my_best_model.hdf5')):
            self.pca = pickle.load(open(os.path.join('modelFit','pca.sav'), 'rb'))
            self.clf = keras.models.load_model(os.path.join('modelFit','my_best_model.hdf5'))
            self.doFit=False
        else:
            self.doFit = True
            self.pca = PCA(n_components=17)
            self.clf= None



    def fit(self):
        df = pd.read_csv(os.path.join('modelFit','EmotionGait.csv'))
        X_dataframe = df.drop(['GaitID', 'Etichetta'], axis=1)
        y_dataframe = df['Etichetta']

        X_dataframe = self.pca.fit_transform(X_dataframe)
        X_dataframe = pd.DataFrame(data=X_dataframe)
        X_train, X_val, y_train, y_val = train_test_split(X_dataframe,
                                                            y_dataframe,
                                                            stratify=y_dataframe,
                                                            test_size=0.20,
                                                            random_state=42)

        num_rows, num_cols = X_train.shape
        y_train_one_hot = to_categorical(y_train, num_classes=4)
        y_val_one_hot = to_categorical(y_val, num_classes=4)

        self.clf = keras.models.Sequential()
        self.clf.add(Dense(32, activation='relu', input_dim=num_cols))
        self.clf.add(Dropout(0.5))
        self.clf.add(Dense(16, activation='relu'))
        self.clf.add(Dropout(0.5))
        self.clf.add(Dense(4, activation='softmax'))

        optimizer = Adam(learning_rate=0.0001)
        self.clf.compile(optimizer=optimizer,
                        loss='categorical_crossentropy',
                        metrics=['accuracy']
                        )

        callback_a = ModelCheckpoint(filepath='modelFit/my_best_model.hdf5', monitor='val_loss', save_best_only=True)
        self.clf.fit(x=X_train,
                    y=y_train_one_hot,
                    validation_data=(X_val, y_val_one_hot),
                    epochs=4000,
                    batch_size=10,
                    callbacks=[callback_a],
                    verbose=0)

        self.clf.load_weights(os.path.join('modelFit','my_best_model.hdf5'))
        y_predict =self.clf.predict(X_val)
        predizioni_classe=self.getEtichette(y_predict)
        print("Accuracy Modello Train:{}".format(classification_report(y_val, predizioni_classe, output_dict=True,zero_division=0)['accuracy']))
        pickle.dump(self.pca, open(os.path.join('modelFit','pca.sav'), 'wb'))

    def predict(self,df):
        if self.doFit:
            print("Eseguo la Fit del modello")
            self.fit()

        df = self.pca.transform(df)
        df = pd.DataFrame(data=df)

        y_predict = self.clf.predict(df)
        predizione_classe=self.getEtichette(y_predict)
        return predizione_classe



    def getEtichette(self,y_predict):
        etichette_classe = [0, 1, 2, 3]
        indici_predetti = np.argmax(y_predict, axis=1)
        mappa_etichette = {etichetta: indice for indice, etichetta in enumerate(etichette_classe)}
        predizioni_classe = [mappa_etichette[etichette_classe[indice]] for indice in indici_predetti]
        return predizioni_classe
