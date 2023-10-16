# -*- coding: utf-8 -*-
"""cox_box.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1MX1qoHDn5e9tSeiYS0wDwQAY51OY1Utp

**Filtro de cox box**
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import PowerTransformer

from google.colab import drive
drive.mount('/content/drive')

#importar datos

test = pd.read_csv('/content/drive/MyDrive/ArchivosColab/test.csv')
train = pd.read_csv('/content/drive/MyDrive/ArchivosColab/train.csv')

train.head()

train.info()

# Como se distribuyen los valores numericos
train.describe()

plt.hist(train['Age'])

plt.hist(train['Fare'])

train['Age'].fillna(value=train['Age'].mean() , inplace=True)
X = train[['Fare','Age']]
Y = train[['Survived']]

X_train, X_test, Y_train, Y_test = train_test_split(X , Y , test_size=0.2 , random_state = 42)

#BOX_COX transform
pt = PowerTransformer(method = "box-cox")

X_train_transformed = pt.fit_transform(X_train+0.000001)
X_test_transformed = pt.transform(X_test+0.000001)

pd.DataFrame({'cols': X_train.columns, 'box_cox_lambdas' : pt.lambdas_})

# Entrenando modelos de regresion logistica
from sklearn.linear_model import LogisticRegression

logreg=LogisticRegression()
logreg.fit(X_train_transformed,Y_train)

from sklearn.metrics import accuracy_score

# Realizar predicciones en el conjunto de prueba
y_pred = logreg.predict(X_test_transformed)

# Evaluar el rendimiento del modelo
accuracy = accuracy_score(Y_test, y_pred)
print("Exactitud del modelo:", accuracy)

#Before and after comparision for Box-Cox Plot
X_train_transformed = pd.DataFrame(X_train_transformed,columns = X_train.columns)
for col in X_train_transformed.columns:
  plt.figure(figsize = (14,4))
  plt.subplot(121)
  sns.distplot(X_train[col])
  plt.title(col)

  plt.subplot(122)
  sns.distplot(X_train_transformed[col])
  plt.title(col)

  plt.show()
